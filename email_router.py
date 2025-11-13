#!/usr/bin/env python3
"""
Email Routing Automation System
স্বয়ংক্রিয় ইমেইল রাউটিং সিস্টেম

This script automatically forwards emails from Commercial Department 
to appropriate insurance companies based on configurable routing rules.
"""

import imaplib
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import yaml
import json
import time
import logging
from datetime import datetime
from pathlib import Path
import re
import os
from typing import List, Dict, Optional

from license_manager import LicenseError, LicenseManager

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('email_router.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EmailRouter:
    """Main email routing automation class"""
    
    def __init__(self, config_path: str = 'config.yaml'):
        """Initialize email router with configuration"""
        self.config = self.load_config(config_path)
        self.routing_rules = self.load_routing_rules()
        self.processed_emails = self.load_processed_emails()
        
    def load_config(self, config_path: str) -> Dict:
        """Load main configuration file"""
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            logger.info("Configuration loaded successfully")
            return config
        except FileNotFoundError:
            logger.error(f"Configuration file {config_path} not found!")
            raise
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def load_routing_rules(self) -> Dict:
        """Load routing rules from rules file"""
        rules_path = self.config.get('routing_rules_file', 'routing_rules.yaml')
        try:
            with open(rules_path, 'r', encoding='utf-8') as f:
                rules = yaml.safe_load(f)
            logger.info(f"Loaded {len(rules.get('rules', []))} routing rules")
            return rules
        except FileNotFoundError:
            logger.warning(f"Routing rules file {rules_path} not found. Creating default.")
            return {'rules': []}
        except Exception as e:
            logger.error(f"Error loading routing rules: {e}")
            return {'rules': []}
    
    def load_processed_emails(self) -> set:
        """Load list of already processed email IDs"""
        processed_file = 'processed_emails.txt'
        try:
            with open(processed_file, 'r') as f:
                return set(line.strip() for line in f)
        except FileNotFoundError:
            return set()
    
    def save_processed_email(self, email_id: str):
        """Save processed email ID to file"""
        with open('processed_emails.txt', 'a') as f:
            f.write(f"{email_id}\n")
        self.processed_emails.add(email_id)
        # Remove from failed emails if it was there
        self.remove_failed_email(email_id)
    
    def save_failed_email(self, email_id: str, error: str):
        """Save failed email for retry"""
        failed_file = 'failed_emails.txt'
        try:
            with open(failed_file, 'a', encoding='utf-8') as f:
                f.write(f"{email_id}|{datetime.now().isoformat()}|{error}\n")
        except Exception as e:
            logger.error(f"Error saving failed email: {e}")
    
    def load_failed_emails(self) -> Dict[str, Dict]:
        """Load failed emails for retry"""
        failed_file = 'failed_emails.txt'
        failed = {}
        try:
            if os.path.exists(failed_file):
                with open(failed_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        parts = line.strip().split('|')
                        if len(parts) >= 2:
                            email_id = parts[0]
                            timestamp = parts[1]
                            error = parts[2] if len(parts) > 2 else 'Unknown error'
                            failed[email_id] = {'timestamp': timestamp, 'error': error}
        except Exception as e:
            logger.error(f"Error loading failed emails: {e}")
        return failed
    
    def remove_failed_email(self, email_id: str):
        """Remove email from failed list after successful processing"""
        failed_file = 'failed_emails.txt'
        try:
            if os.path.exists(failed_file):
                with open(failed_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                with open(failed_file, 'w', encoding='utf-8') as f:
                    for line in lines:
                        if not line.startswith(f"{email_id}|"):
                            f.write(line)
        except Exception as e:
            logger.error(f"Error removing failed email: {e}")
    
    def connect_imap(self) -> imaplib.IMAP4_SSL:
        """Connect to IMAP server for reading emails"""
        try:
            imap_server = self.config['email']['imap_server']
            imap_port = self.config['email'].get('imap_port', 993)
            email_address = self.config['email']['address']
            password = self.config['email']['password']
            
            mail = imaplib.IMAP4_SSL(imap_server, imap_port)
            mail.login(email_address, password)
            logger.info("Successfully connected to IMAP server")
            return mail
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise
    
    def connect_smtp(self):
        """Connect to SMTP server for sending emails
        
        Handles both SSL (port 465) and STARTTLS (port 587) connections
        """
        try:
            smtp_server = self.config['email']['smtp_server']
            smtp_port = self.config['email'].get('smtp_port', 587)
            email_address = self.config['email']['address']
            password = self.config['email']['password']
            
            # Port 465 uses SSL/TLS directly (SMTP_SSL)
            # Port 587 uses STARTTLS (SMTP with starttls())
            if smtp_port == 465:
                logger.info(f"Connecting to SMTP server {smtp_server}:{smtp_port} using SSL...")
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
                server.login(email_address, password)
                logger.info("Successfully connected to SMTP server (SSL)")
            else:
                # Default: port 587 or other ports with STARTTLS
                logger.info(f"Connecting to SMTP server {smtp_server}:{smtp_port} using STARTTLS...")
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
                server.login(email_address, password)
                logger.info("Successfully connected to SMTP server (STARTTLS)")
            
            return server
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            logger.error(f"Server: {smtp_server}, Port: {smtp_port}")
            raise
    
    def find_matching_rule(self, email_msg: email.message.Message) -> Optional[Dict]:
        """Find matching routing rule for an email"""
        subject = email_msg.get('Subject', '')
        from_addr = email_msg.get('From', '')
        body = self.get_email_body(email_msg)
        
        # Check if from Commercial Department
        commercial_emails = self.config.get('commercial_department', {}).get('emails', [])
        
        from_matches = False
        for comm_email in commercial_emails:
            if comm_email.lower() in from_addr.lower():
                from_matches = True
                break
        
        if not from_matches:
            logger.debug(f"Email not from Commercial Department: {from_addr}")
            return None
        
        # Find matching rule
        for rule in self.routing_rules.get('rules', []):
            if not rule.get('enabled', True):
                continue
                
            # Check rule conditions
            if self.rule_matches(rule, subject, from_addr, body):
                logger.info(f"Found matching rule: {rule.get('name', 'Unnamed')}")
                return rule
        
        # Check default rule
        default_rule = self.routing_rules.get('default_rule')
        if default_rule and default_rule.get('enabled', True):
            logger.info("Using default routing rule")
            return default_rule
        
        logger.warning("No matching rule found for email")
        return None
    
    def rule_matches(self, rule: Dict, subject: str, from_addr: str, body: str) -> bool:
        """Check if a rule matches the email"""
        match_type = rule.get('match_type', 'any')
        conditions = rule.get('conditions', {})
        
        matches = []
        
        # Check subject keywords
        if 'subject_keywords' in conditions:
            keywords = conditions['subject_keywords']
            subject_match = any(keyword.lower() in subject.lower() for keyword in keywords)
            matches.append(subject_match)
        
        # Check body keywords
        if 'body_keywords' in conditions:
            keywords = conditions['body_keywords']
            body_match = any(keyword.lower() in body.lower() for keyword in keywords)
            matches.append(body_match)
        
        # Check sender
        if 'from_contains' in conditions:
            sender_patterns = conditions['from_contains']
            sender_match = any(pattern.lower() in from_addr.lower() for pattern in sender_patterns)
            matches.append(sender_match)
        
        # Check subject regex
        if 'subject_regex' in conditions:
            regex_pattern = conditions['subject_regex']
            try:
                regex_match = bool(re.search(regex_pattern, subject, re.IGNORECASE))
                matches.append(regex_match)
            except re.error:
                logger.error(f"Invalid regex pattern: {regex_pattern}")
        
        # If no conditions specified, don't match
        if not matches:
            return False
        
        # Apply match type logic
        if match_type == 'all':
            return all(matches)
        elif match_type == 'any':
            return any(matches)
        else:
            return any(matches)
    
    def get_email_body(self, email_msg: email.message.Message) -> str:
        """Extract email body text"""
        body = ""
        try:
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    content_type = part.get_content_type()
                    if content_type == "text/plain":
                        try:
                            body += part.get_payload(decode=True).decode()
                        except:
                            pass
            else:
                body = email_msg.get_payload(decode=True).decode()
        except Exception as e:
            logger.error(f"Error extracting email body: {e}")
        return body
    
    def forward_email(self, email_msg: email.message.Message, rule: Dict):
        """Forward email according to routing rule"""
        try:
            # Get recipients
            insurance_companies = rule.get('forward_to', [])
            accounts_dept_config = self.config.get('accounts_department', {})
            
            # Support both old format (email) and new format (emails list)
            accounts_dept_emails = accounts_dept_config.get('emails', [])
            if not accounts_dept_emails:
                # Backward compatibility: check for single 'email' field
                single_email = accounts_dept_config.get('email')
                if single_email:
                    accounts_dept_emails = [single_email]
            
            if not insurance_companies:
                logger.warning("No insurance companies specified in rule")
                return
            
            # Connect to SMTP
            smtp = self.connect_smtp()
            
            # Create forwarded message
            forward_msg = MIMEMultipart()
            forward_msg['From'] = self.config['email']['address']
            forward_msg['To'] = ', '.join(insurance_companies)
            
            # Add CC to Accounts Department (multiple emails supported)
            recipients = list(insurance_companies)
            if accounts_dept_emails:
                forward_msg['Cc'] = ', '.join(accounts_dept_emails)
                recipients.extend(accounts_dept_emails)
            
            # Original subject with FWD prefix if not already there
            original_subject = email_msg.get('Subject', 'No Subject')
            if not original_subject.startswith('Fwd:') and not original_subject.startswith('FW:'):
                forward_msg['Subject'] = f"Fwd: {original_subject}"
            else:
                forward_msg['Subject'] = original_subject
            
            # Build forwarded message body
            forward_body = f"""
---------- Forwarded message ---------
From: {email_msg.get('From', 'Unknown')}
Date: {email_msg.get('Date', 'Unknown')}
Subject: {original_subject}

{self.get_email_body(email_msg)}
"""
            
            forward_msg.attach(MIMEText(forward_body, 'plain', 'utf-8'))
            
            # Attach any attachments from original email
            if email_msg.is_multipart():
                for part in email_msg.walk():
                    if part.get_content_maintype() == 'multipart':
                        continue
                    if part.get('Content-Disposition') is None:
                        continue
                    
                    filename = part.get_filename()
                    if filename:
                        attachment = MIMEBase(part.get_content_type().split('/')[0], 
                                            part.get_content_type().split('/')[1])
                        attachment.set_payload(part.get_payload(decode=True))
                        encoders.encode_base64(attachment)
                        attachment.add_header('Content-Disposition', f'attachment; filename={filename}')
                        forward_msg.attach(attachment)
            
            # Send email
            smtp.send_message(forward_msg, 
                            from_addr=self.config['email']['address'],
                            to_addrs=recipients)
            
            smtp.quit()
            
            logger.info(f"Successfully forwarded email to: {', '.join(insurance_companies)}")
            
            # Log the routing action
            self.log_routing_action(email_msg, rule, insurance_companies)
            
        except Exception as e:
            logger.error(f"Error forwarding email: {e}")
            raise
    
    def log_routing_action(self, email_msg: email.message.Message, rule: Dict, recipients: List[str]):
        """Log routing action to file"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'from': email_msg.get('From', 'Unknown'),
            'subject': email_msg.get('Subject', 'No Subject'),
            'rule_name': rule.get('name', 'Unnamed'),
            'forwarded_to': recipients
        }
        
        with open('routing_log.json', 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + '\n')
    
    def process_inbox(self, include_read=False):
        """Process incoming emails in inbox
        
        Args:
            include_read: If True, also process read emails that haven't been successfully forwarded
        """
        try:
            mail = self.connect_imap()
            mail.select('INBOX')
            
            # Load failed emails for retry
            failed_emails = self.load_failed_emails()
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.error("Failed to search emails")
                return
            
            email_ids = messages[0].split()
            logger.info(f"Found {len(email_ids)} unread emails")
            
            # Always retry failed emails (even if they are read)
            if failed_emails:
                status_all, messages_all = mail.search(None, 'ALL')
                if status_all == 'OK':
                    all_email_ids = messages_all[0].split()
                    # Add failed emails that are not in unread list
                    for email_id in all_email_ids:
                        email_id_str = email_id.decode()
                        if email_id_str in failed_emails and email_id_str not in email_ids:
                            email_ids.append(email_id)
                    if failed_emails:
                        logger.info(f"Retrying {len(failed_emails)} previously failed emails")
            
            for email_id in email_ids:
                email_id_str = email_id.decode()
                
                # Skip if already processed successfully
                if email_id_str in self.processed_emails:
                    continue
                
                # Process failed emails even if they are read
                is_failed_email = email_id_str in failed_emails
                
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        logger.error(f"Failed to fetch email {email_id_str}")
                        continue
                    
                    # Parse email
                    email_msg = email.message_from_bytes(msg_data[0][1])
                    
                    logger.info(f"Processing email: {email_msg.get('Subject', 'No Subject')}")
                    
                    # Find matching rule
                    rule = self.find_matching_rule(email_msg)
                    
                    if rule:
                        # Forward email (only mark as processed if successful)
                        try:
                            self.forward_email(email_msg, rule)
                            
                            # Only mark as processed AFTER successful forward
                            self.save_processed_email(email_id_str)
                            
                            # Optional: Mark as read ONLY after successful forward
                            if self.config.get('mark_as_read', True):
                                mail.store(email_id, '+FLAGS', '\\Seen')
                                
                        except Exception as forward_error:
                            # Forward failed - don't mark as processed
                            logger.error(f"Failed to forward email {email_id_str}: {forward_error}")
                            # Save failed email for retry
                            self.save_failed_email(email_id_str, str(forward_error))
                            # Don't mark as read, so it will be retried
                            continue
                    else:
                        logger.info(f"No routing rule matched for email: {email_msg.get('Subject')}")
                        # Optionally mark as read or flag for manual review
                        if self.config.get('mark_unmatched_as_read', False):
                            mail.store(email_id, '+FLAGS', '\\Seen')
                    
                except Exception as e:
                    logger.error(f"Error processing email {email_id_str}: {e}")
                    continue
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            logger.error(f"Error processing inbox: {e}")
            raise
    
    def run_once(self):
        """Run email processing once"""
        logger.info("Starting email routing process...")
        try:
            self.process_inbox()
            logger.info("Email routing process completed")
        except Exception as e:
            logger.error(f"Error in email routing: {e}")
    
    def run_continuous(self, interval: int = 60):
        """Run email processing continuously"""
        logger.info(f"Starting continuous email routing (checking every {interval} seconds)...")
        
        while True:
            try:
                self.run_once()
                logger.info(f"Waiting {interval} seconds before next check...")
                time.sleep(interval)
            except KeyboardInterrupt:
                logger.info("Email router stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in continuous mode: {e}")
                logger.info(f"Retrying in {interval} seconds...")
                time.sleep(interval)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Email Routing Automation System')
    parser.add_argument('--config', default='config.yaml', help='Configuration file path')
    parser.add_argument('--once', action='store_true', help='Run once and exit')
    parser.add_argument('--interval', type=int, default=60, help='Check interval in seconds (default: 60)')
    
    args = parser.parse_args()
    
    try:
        # Enforce license validation before starting the core workflow.
        license_context = LicenseManager().ensure_valid_license()
        logger.info(
            "License validated. Expires at %s",
            license_context.expires_at.isoformat(),
        )

        router = EmailRouter(config_path=args.config)
        
        if args.once:
            router.run_once()
        else:
            router.run_continuous(interval=args.interval)
            
    except LicenseError as exc:
        logger.error("License validation failed: %s", exc)
        print("License Expired" if "expired" in str(exc).lower() else str(exc))
        return 2
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
