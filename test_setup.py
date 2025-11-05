#!/usr/bin/env python3
"""
Setup Validation Script
সেটআপ ভ্যালিডেশন স্ক্রিপ্ট

Run this script to validate your email routing system setup.
"""

import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(text)
    print("="*60)

def print_success(text):
    print(f"✓ {text}")

def print_error(text):
    print(f"✗ {text}")

def print_warning(text):
    print(f"⚠ {text}")

def test_python_version():
    """Test Python version"""
    print_header("Testing Python Version / Python ভার্সন চেক")
    
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    print(f"Python Version: {version_str}")
    
    if version.major >= 3 and version.minor >= 7:
        print_success("Python version is compatible")
        return True
    else:
        print_error("Python 3.7 or higher is required")
        return False

def test_dependencies():
    """Test if required packages are installed"""
    print_header("Testing Dependencies / ডিপেন্ডেন্সি চেক")
    
    required = ['yaml', 'email', 'imaplib', 'smtplib']
    all_ok = True
    
    for module in required:
        try:
            __import__(module)
            print_success(f"{module} is installed")
        except ImportError:
            print_error(f"{module} is NOT installed")
            all_ok = False
    
    return all_ok

def test_config_file():
    """Test if config.yaml exists and is valid"""
    print_header("Testing Configuration File / কনফিগারেশন ফাইল চেক")
    
    if not os.path.exists('config.yaml'):
        print_error("config.yaml not found!")
        print("  Create it by copying from example_config.yaml")
        return False
    
    print_success("config.yaml exists")
    
    try:
        import yaml
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        # Check required fields
        errors = []
        
        if 'email' not in config:
            errors.append("'email' section missing")
        else:
            email_config = config['email']
            if email_config.get('address') == 'your-email@example.com':
                errors.append("Email address not configured (still showing default)")
            if email_config.get('password') == 'your-app-password':
                errors.append("Email password not configured (still showing default)")
        
        if 'commercial_department' not in config:
            errors.append("'commercial_department' section missing")
        
        if 'accounts_department' not in config:
            errors.append("'accounts_department' section missing")
        
        if errors:
            print_error("Configuration has issues:")
            for error in errors:
                print(f"  - {error}")
            return False
        else:
            print_success("Configuration is valid")
            return True
            
    except Exception as e:
        print_error(f"Error reading config.yaml: {e}")
        return False

def test_routing_rules():
    """Test if routing_rules.yaml exists and is valid"""
    print_header("Testing Routing Rules / রাউটিং রুলস চেক")
    
    if not os.path.exists('routing_rules.yaml'):
        print_error("routing_rules.yaml not found!")
        return False
    
    print_success("routing_rules.yaml exists")
    
    try:
        import yaml
        with open('routing_rules.yaml', 'r', encoding='utf-8') as f:
            rules = yaml.safe_load(f)
        
        if 'rules' not in rules:
            print_error("No 'rules' section found")
            return False
        
        rules_list = rules.get('rules', [])
        enabled_rules = [r for r in rules_list if r.get('enabled', True)]
        
        print(f"  Total rules: {len(rules_list)}")
        print(f"  Enabled rules: {len(enabled_rules)}")
        
        if len(enabled_rules) == 0:
            print_warning("No enabled rules found. Email routing will not work.")
            print("  Run: python3 manage_rules.py to add rules")
            return False
        
        print_success(f"{len(enabled_rules)} enabled rule(s) found")
        return True
        
    except Exception as e:
        print_error(f"Error reading routing_rules.yaml: {e}")
        return False

def test_email_connection():
    """Test email connection"""
    print_header("Testing Email Connection / ইমেইল কানেকশন চেক")
    
    try:
        import yaml
        with open('config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        email_config = config['email']
        address = email_config.get('address', '')
        password = email_config.get('password', '')
        
        # Skip if default values
        if address == 'your-email@example.com' or password == 'your-app-password':
            print_warning("Email credentials not configured. Skipping connection test.")
            return None
        
        print("Testing IMAP connection...")
        import imaplib
        
        imap_server = email_config.get('imap_server', 'imap.gmail.com')
        imap_port = email_config.get('imap_port', 993)
        
        mail = imaplib.IMAP4_SSL(imap_server, imap_port)
        mail.login(address, password)
        mail.logout()
        
        print_success("IMAP connection successful")
        
        print("Testing SMTP connection...")
        import smtplib
        
        smtp_server = email_config.get('smtp_server', 'smtp.gmail.com')
        smtp_port = email_config.get('smtp_port', 587)
        
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(address, password)
        server.quit()
        
        print_success("SMTP connection successful")
        return True
        
    except Exception as e:
        print_error(f"Email connection failed: {e}")
        print("\nTroubleshooting:")
        print("  - Check email address and password")
        print("  - For Gmail, use App Password (not regular password)")
        print("  - Enable 2-Step Verification for Gmail")
        print("  - Check IMAP/SMTP server settings")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print_header("Testing File Structure / ফাইল স্ট্রাকচার চেক")
    
    required_files = [
        'email_router.py',
        'manage_rules.py',
        'config.yaml',
        'routing_rules.yaml',
        'requirements.txt'
    ]
    
    all_ok = True
    for filename in required_files:
        if os.path.exists(filename):
            print_success(f"{filename} exists")
        else:
            print_error(f"{filename} NOT found")
            all_ok = False
    
    return all_ok

def main():
    """Main test function"""
    print("\n")
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║   EMAIL ROUTING SYSTEM - SETUP VALIDATION                 ║")
    print("║   ইমেইল রাউটিং সিস্টেম - সেটআপ ভ্যালিডেশন              ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    
    results = {}
    
    # Run all tests
    results['python'] = test_python_version()
    results['dependencies'] = test_dependencies()
    results['files'] = test_file_structure()
    results['config'] = test_config_file()
    results['rules'] = test_routing_rules()
    results['connection'] = test_email_connection()
    
    # Summary
    print_header("Test Summary / টেস্ট সামারি")
    
    passed = sum(1 for v in results.values() if v is True)
    failed = sum(1 for v in results.values() if v is False)
    skipped = sum(1 for v in results.values() if v is None)
    
    print(f"\nPassed:  {passed}")
    print(f"Failed:  {failed}")
    print(f"Skipped: {skipped}")
    
    if failed == 0:
        print("\n" + "="*60)
        print("✓ All tests passed! Your setup is ready.")
        print("✓ সব টেস্ট পাস হয়েছে! আপনার সেটআপ প্রস্তুত।")
        print("="*60)
        print("\nYou can now run:")
        print("  python3 email_router.py --once    (test mode)")
        print("  python3 email_router.py           (continuous mode)")
        return 0
    else:
        print("\n" + "="*60)
        print("✗ Some tests failed. Please fix the issues above.")
        print("✗ কিছু টেস্ট ফেইল হয়েছে। উপরের সমস্যাগুলো ঠিক করুন।")
        print("="*60)
        print("\nRefer to README_BANGLA.md for detailed setup instructions.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
