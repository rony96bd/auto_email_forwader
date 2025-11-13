#!/usr/bin/env python3
"""
Centralized license verification utilities for the Email Router application.

The module is responsible for:
    * Loading the local license key
    * Contacting the remote license server
    * Verifying server responses (integrity + signature)
    * Performing code integrity checks to make tampering harder
    * Providing cached grace-period support for temporary outages
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import logging
import os
import platform
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional, Tuple

import requests


logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# Configuration constants
# -----------------------------------------------------------------------------

APP_IDENTIFIER = "auto-email-router"
APP_VERSION = "1.0.0"

DEFAULT_LICENSE_KEY_URL = "https://epagebd.com/license.key"
DEFAULT_LICENSE_ENDPOINT = "https://epagebd.com/license-server/public/index.php"

LICENSE_KEY_ENV = "LICENSE_KEY"
LICENSE_KEY_URL_ENV = "LICENSE_KEY_URL"
LICENSE_ENDPOINT_ENV = "LICENSE_SERVER_URL"

LICENSE_KEY_FILE = "license.key"
LICENSE_CACHE_FILE = ".license_cache.json"

# Number of seconds a cached license can be reused when the remote service fails.
CACHE_MAX_AGE_SECONDS = 6 * 60 * 60  # 6 hours

# Files that must stay untouched; the server provides the expected hashes.
CRITICAL_FILES = (
    "email_router.py",
    "gui_app.py",
    "license_manager.py",
)

# Secret used to validate the HMAC signature coming from the licensing server.
# The real value is split in several fragments to hinder trivial string searches.
_SECRET_PARTS = (
    "bGljZW5zZQ==",          # license
    "LXN5cw==",              # -sys
    "LXNlY3JldC0yMDI1"       # -secret-2025
)


class LicenseError(RuntimeError):
    """Raised when the license is invalid, expired, or cannot be verified."""


class LicenseTamperingError(LicenseError):
    """Raised when application integrity checks indicate tampering."""


@dataclass(frozen=True)
class LicenseContext:
    """Minimal information about the validated license."""

    license_key: str
    expires_at: datetime
    payload: Dict[str, object]


class LicenseManager:
    """High-level license management helper."""

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        server_url: Optional[str] = None,
        cache_ttl_seconds: int = CACHE_MAX_AGE_SECONDS,
    ) -> None:
        self.base_dir = base_dir or Path(__file__).resolve().parent
        self.server_url = server_url or os.environ.get(
            LICENSE_ENDPOINT_ENV, DEFAULT_LICENSE_ENDPOINT
        )
        self.cache_ttl_seconds = cache_ttl_seconds

        self.license_key = self._load_license_key()
        self.cache_path = self.base_dir / LICENSE_CACHE_FILE

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def ensure_valid_license(self) -> LicenseContext:
        """
        Validate the license with the remote server. Cache is disabled - 
        license must be validated online every time.

        Raises:
            LicenseError: for invalid/expired licenses or when server is unreachable.
            LicenseTamperingError: if integrity checks fail.
        """
        logger.debug("Starting license verification workflow (cache disabled)")

        try:
            payload = self._fetch_remote_license()
            logger.debug("License payload fetched from remote endpoint")
            context = self._validate_payload(payload)
            logger.info("License validated successfully via remote server")
            return context
        except Exception as exc:  # noqa: BLE001 - deliberate aggregation
            logger.error("Remote license validation failed: %s", exc)
            raise LicenseError(
                f"License verification failed. Internet connection required. Error: {exc}"
            ) from exc

    # --------------------------------------------------------------------- #
    # Helpers: license key management
    # --------------------------------------------------------------------- #
    def _load_license_key(self) -> str:
        env_value = os.environ.get(LICENSE_KEY_ENV)
        if env_value:
            logger.debug("Using license key from environment variable")
            return env_value.strip()

        key_file = self.base_dir / LICENSE_KEY_FILE
        if key_file.exists():
            key = key_file.read_text(encoding="utf-8").strip()
            if key:
                logger.debug("Using license key from file %s", key_file)
                return key

        remote_key = self._fetch_remote_license_key()
        if remote_key:
            return remote_key

        raise LicenseError(
            "License key not found. Set the LICENSE_KEY environment variable, "
            f"place the key inside {LICENSE_KEY_FILE}, or configure the "
            f"{LICENSE_KEY_URL_ENV} environment variable to point to a remote key."
        )

    def _fetch_remote_license_key(self) -> Optional[str]:
        url = os.environ.get(LICENSE_KEY_URL_ENV, DEFAULT_LICENSE_KEY_URL)
        if not url:
            return None

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            key = response.text.strip()
            if key:
                logger.debug("Using license key fetched from %s", url)
                return key
            logger.warning("Remote license key at %s is empty", url)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Unable to fetch license key from %s: %s", url, exc)

        return None

    # --------------------------------------------------------------------- #
    # Helpers: remote interaction & caching
    # --------------------------------------------------------------------- #
    def _fetch_remote_license(self) -> Dict[str, object]:
        payload = {
            "app_id": APP_IDENTIFIER,
            "app_version": APP_VERSION,
            "license_key": self._hash_license_key(self.license_key),
            "machine_fingerprint": self._machine_fingerprint(),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        response = requests.post(
            self.server_url,
            json=payload,
            timeout=10,
        )
        response.raise_for_status()

        try:
            data = response.json()
        except Exception as exc:  # noqa: BLE001 - handle JSON decoding errors
            raise LicenseError(f"License server returned invalid JSON: {exc}") from exc

        if not isinstance(data, dict):
            raise LicenseError("Unexpected payload received from license server")

        return data

    def _read_cache(self) -> Optional[Dict[str, object]]:
        if not self.cache_path.exists():
            return None

        try:
            cached = json.loads(self.cache_path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001 - handle malformed cache
            logger.warning("Failed to read cached license file: %s", exc)
            return None

        payload = cached.get("payload")
        fetched_at = cached.get("fetched_at")

        if not isinstance(payload, dict) or not isinstance(fetched_at, (int, float)):
            logger.warning("Cached license file format is invalid")
            return None

        self._cached_fetched_at = float(fetched_at)
        return payload

    def _write_cache(self, payload: Dict[str, object]) -> None:
        cached = {
            "payload": payload,
            "fetched_at": time.time(),
        }
        try:
            self.cache_path.write_text(
                json.dumps(cached, ensure_ascii=False), encoding="utf-8"
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Unable to persist license cache: %s", exc)

        # Store retrieval time for later freshness checks
        self._cached_fetched_at = cached["fetched_at"]

    def _cache_is_fresh(self) -> bool:
        fetched_at = getattr(self, "_cached_fetched_at", None)
        if fetched_at is None:
            return False

        age = time.time() - fetched_at
        logger.debug("Cached license age: %ss", int(age))
        return age <= self.cache_ttl_seconds

    # --------------------------------------------------------------------- #
    # Helpers: payload verification and integrity checks
    # --------------------------------------------------------------------- #
    def _validate_payload(
        self,
        payload: Dict[str, object],
        *,
        from_cache: bool = False,
    ) -> LicenseContext:
        payload_copy = dict(payload)

        signature = payload_copy.pop("signature", None)
        if not isinstance(signature, str):
            raise LicenseError("License payload missing digital signature")

        self._verify_signature(payload_copy, signature)

        status = payload_copy.get("status")
        if status != "active":
            message = payload_copy.get("message", "License not active")
            raise LicenseError(f"License server rejected the license: {message}")

        expires_at = self._parse_iso_datetime(payload_copy.get("expires_at"))
        if expires_at <= datetime.now(timezone.utc):
            raise LicenseError("License has expired")

        allowed_app = payload_copy.get("app_id")
        if allowed_app not in (APP_IDENTIFIER, "*"):
            raise LicenseError("License is not valid for this application")

        allowed_versions = payload_copy.get("allowed_versions")
        if isinstance(allowed_versions, (list, tuple)) and allowed_versions:
            if APP_VERSION not in allowed_versions and "*" not in allowed_versions:
                raise LicenseError("Current application version is not licensed")

        # Integrity check of critical files
        self._validate_code_hashes(payload_copy.get("code_hashes", {}))

        license_key_hash = payload_copy.get("license_key_hash")
        expected_hash = self._hash_license_key(self.license_key)
        if license_key_hash != expected_hash:
            raise LicenseError("License key mismatch detected")

        if not from_cache:
            # Reset cached timestamp to the freshly fetched value
            self._cached_fetched_at = time.time()

        return LicenseContext(
            license_key=self.license_key,
            expires_at=expires_at,
            payload=payload_copy,
        )

    def _verify_signature(self, payload: Dict[str, object], signature: str) -> None:
        try:
            signature_bytes = base64.b64decode(signature)
        except Exception as exc:  # noqa: BLE001
            raise LicenseError("Invalid license signature encoding") from exc

        serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode(
            "utf-8"
        )
        secret = self._signature_secret()
        expected = hmac.new(secret, serialized, hashlib.sha256).digest()

        if not hmac.compare_digest(expected, signature_bytes):
            raise LicenseTamperingError("License signature verification failed")

    def _validate_code_hashes(self, code_hashes: object) -> None:
        if not isinstance(code_hashes, dict):
            raise LicenseError("License payload missing code integrity information")

        for relative_path in CRITICAL_FILES:
            expected_hash = code_hashes.get(relative_path)
            if not isinstance(expected_hash, str):
                raise LicenseTamperingError(
                    f"Integrity hash missing for critical file: {relative_path}"
                )

            actual_hash = self._compute_file_hash(relative_path)
            if actual_hash != expected_hash:
                raise LicenseTamperingError(
                    f"Critical file modified: {relative_path}. "
                    "Reinstallation or re-licensing is required."
                )

    def _compute_file_hash(self, relative_path: str) -> str:
        file_path = self.base_dir / relative_path
        if not file_path.exists():
            raise LicenseTamperingError(f"Required file not found: {relative_path}")

        sha = hashlib.sha256()
        with file_path.open("rb") as file_handle:
            for chunk in iter(lambda: file_handle.read(64 * 1024), b""):
                sha.update(chunk)
        return sha.hexdigest()

    # --------------------------------------------------------------------- #
    # Helpers: utilities
    # --------------------------------------------------------------------- #
    def _signature_secret(self) -> bytes:
        parts = [base64.b64decode(p) for p in _SECRET_PARTS]
        return b"".join(parts)

    def _hash_license_key(self, license_key: str) -> str:
        return hashlib.sha256(license_key.encode("utf-8")).hexdigest()

    def _machine_fingerprint(self) -> str:
        node = platform.node()
        mac = uuid.getnode()
        system = platform.system()
        version = platform.version()
        release = platform.release()

        raw = f"{node}|{mac}|{system}|{version}|{release}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def _parse_iso_datetime(self, value: object) -> datetime:
        if not isinstance(value, str):
            raise LicenseError("License payload missing expiry timestamp")

        iso_value = value.strip()
        if iso_value.endswith("Z"):
            iso_value = iso_value[:-1] + "+00:00"

        try:
            parsed = datetime.fromisoformat(iso_value)
        except ValueError as exc:
            raise LicenseError(f"Invalid expiry timestamp: {value}") from exc

        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)

        return parsed.astimezone(timezone.utc)


def enforce_license() -> LicenseContext:
    """
    Convenience helper to enforce a valid license quickly.

    Raises:
        LicenseError
    """
    manager = LicenseManager()
    return manager.ensure_valid_license()


__all__ = [
    "LicenseError",
    "LicenseManager",
    "LicenseTamperingError",
    "LicenseContext",
    "enforce_license",
]


