# Email Routing System - Complete Documentation
# স্বয়ংক্রিয় ইমেইল রাউটিং সিস্টেম - সম্পূর্ণ ডকুমেন্টেশন

---

## 📋 Table of Contents / বিষয়সূচি

1. [Introduction / পরিচিতি](#introduction)
2. [Quick Start / দ্রুত শুরু](#quick-start)
3. [Features / বৈশিষ্ট্য](#features)
4. [Installation / ইনস্টলেশন](#installation)
5. [Configuration / কনফিগারেশন](#configuration)
6. [GUI Guide / GUI গাইড](#gui-guide)
7. [Routing Rules / রাউটিং রুলস](#routing-rules)
8. [Running the System / সিস্টেম চালু করা](#running)
9. [Project Structure / প্রকল্পের গঠন](#project-structure)
10. [Alternative Solutions / বিকল্প সমাধান](#alternatives)
11. [Update History / আপডেটের ইতিহাস](#updates)
12. [Troubleshooting / সমস্যা সমাধান](#troubleshooting)
13. [FAQ / প্রশ্নোত্তর](#faq)

---

## Introduction / পরিচিতি {#introduction}

An automated email forwarding system that routes emails from Commercial Department to appropriate insurance companies based on configurable rules.

কমার্শিয়াল ডিপার্টমেন্ট থেকে আসা ইমেইল স্বয়ংক্রিয়ভাবে সঠিক ইন্সুরেন্স কোম্পানিতে পাঠানোর সম্পূর্ণ সমাধান।

### How It Works / কিভাবে কাজ করে

```
Commercial Department
        ↓
  Your Email Account
        ↓
  Email Router (Automated)
        ↓
  Checks Rules
        ↓
  Forwards to Insurance Company
        +
  CC to Accounts Department
```

---

## Quick Start / দ্রুত শুরু {#quick-start}

### Step 1: Setup (2 minutes)

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

### Step 2: Gmail App Password (1 minute)

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Search for "App passwords"
4. Create a new App Password
5. Copy the password

### Step 3: Configure (1 minute)

Edit `config.yaml`:

```yaml
email:
  address: "your-email@gmail.com"
  password: "your-app-password-here"
  imap_server: "imap.gmail.com"
  smtp_server: "smtp.gmail.com"

commercial_department:
  emails:
    - "commercial@yourcompany.com"

accounts_department:
  email: "accounts@yourcompany.com"
```

### Step 4: Create First Rule (1 minute)

**Using GUI:**
```bash
# Windows
run_gui.bat

# Linux/Mac
./run_gui.sh
```

Then:
1. Go to **Rules** tab
2. Click **➕ Add Rule**
3. Use **Quick Rule** tab for simple forwarding
4. Save

**Using CLI:**
```bash
python3 manage_rules.py
# Select option 2 (Add new rule)
```

### Step 5: Test (30 seconds)

```bash
# Test mode (run once)
python3 email_router.py --once
```

### Step 6: Run Continuously

**Using GUI:**
- Click **▶ Start** button in the header

**Using CLI:**
```bash
# Continuous mode (default: check every 60 seconds)
python3 email_router.py
```

---

## Features / বৈশিষ্ট্য {#features}

✅ **Automatic Email Forwarding** - No manual work required  
✅ **Configurable Rules** - Easy rule management  
✅ **Multiple Conditions** - Subject, Body, Sender based rules  
✅ **Multiple Recipients** - Forward to multiple insurance companies  
✅ **Accounts Department CC** - Automatic CC  
✅ **Comprehensive Logging** - Full activity log  
✅ **Easy Management** - CLI tool and GUI  
✅ **Bengali Keywords Support** - Full Unicode support  
✅ **Regex Pattern Matching** - Advanced pattern matching  
✅ **Modern GUI** - Beautiful graphical interface  
✅ **Quick Rule Creation** - One-click rule setup  
✅ **Failed Email Retry** - Automatic retry mechanism  
✅ **SMTP SSL/TLS Support** - Port 465 and 587 support  

---

## Installation / ইনস্টলেশন {#installation}

### Requirements / প্রয়োজনীয় সফটওয়্যার

- **Python 3.7 or higher**
  - Windows: Download from https://www.python.org/downloads/
  - Linux/Mac: Usually pre-installed

- **Git** (if cloning repository)

### Setup Scripts

The setup script automatically:
- Creates virtual environment
- Installs required packages
- Creates necessary files

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Windows:**
```cmd
setup.bat
```

---

## Configuration / কনফিগারেশন {#configuration}

### Email Configuration (`config.yaml`)

#### Gmail Setup

1. Go to: https://myaccount.google.com/security
2. Enable **2-Step Verification**
3. Create **App Password**
4. Use that password in `config.yaml`

```yaml
email:
  address: "your-email@gmail.com"
  password: "your-app-password"
  imap_server: "imap.gmail.com"
  imap_port: 993
  smtp_server: "smtp.gmail.com"
  smtp_port: 587
```

#### Other Email Providers

**Outlook/Office365:**
```yaml
imap_server: "outlook.office365.com"
smtp_server: "smtp.office365.com"
imap_port: 993
smtp_port: 587
```

**Yahoo:**
```yaml
imap_server: "imap.mail.yahoo.com"
smtp_server: "smtp.mail.yahoo.com"
imap_port: 993
smtp_port: 587
```

**Custom Domain (e.g., epagebd.com):**
```yaml
imap_server: "mail.epagebd.com"
smtp_server: "mail.epagebd.com"
imap_port: 993
smtp_port: 465  # Most custom domains use SSL (port 465)
```

**Important:** Port 465 uses SSL/TLS directly, while port 587 uses STARTTLS. The system automatically detects this.

### Commercial Department

```yaml
commercial_department:
  emails:
    - "commercial@yourcompany.com"
    - "commercial.dept@yourcompany.com"
```

### Accounts Department

```yaml
accounts_department:
  email: "accounts@yourcompany.com"
```

### Processing Options

```yaml
mark_as_read: true              # Mark processed emails as read
mark_unmatched_as_read: false   # Don't mark unmatched emails
check_interval: 60              # Check every 60 seconds
```

---

## GUI Guide / GUI গাইড {#gui-guide}

### Starting the GUI

**Windows:**
```bash
run_gui.bat
```
Or directly:
```bash
python gui_app.py
```

**Linux/Mac:**
```bash
chmod +x run_gui.sh
./run_gui.sh
```
Or directly:
```bash
python3 gui_app.py
```

### GUI Features

#### 1. Dashboard

- **Statistics**: Total Rules, Enabled Rules, Last Check, Failed Emails
- **Quick Actions**: Run Once, Refresh, Retry Failed Emails, Manage Rules

#### 2. Configuration Tab

Configure all settings:
- **Email Settings**: Address, Password, IMAP/SMTP Server & Port
- **Email Provider Auto-Detection**: Automatically fills settings for Gmail, Outlook, Yahoo, or custom domains
- **Password Helper**: Auto-removes spaces from App Passwords
- **Commercial Department**: Email addresses (one per line)
- **Accounts Department**: CC recipient email
- **Processing Options**: Mark as read, check interval

**Save Configuration** button to save all changes.

#### 3. Rules Tab

Manage routing rules:

**Add Rule:**
1. Click **➕ Add Rule**
2. **Quick Rule Tab** (Default):
   - Select Commercial Department Email from dropdown
   - Enter Insurance Department Email
   - Rule Name (optional - auto-generates)
   - Save
   
   **Quick Rule**: All emails from a specific Commercial Department email will be forwarded to a specific Insurance Department email.
   
3. **Advanced Rule Tab**:
   - Rule Name
   - Match Type (Any/All)
   - Conditions:
     - Subject Keywords
     - Body Keywords
     - From Contains
     - Subject Regex (optional)
   - Forward To (one per line)
   - Save

**Edit Rule:**
1. Select rule from list
2. Click **✏️ Edit**
3. Modify and save

**Toggle Enable/Disable:**
1. Select rule
2. Click **🔄 Toggle**

**Delete Rule:**
1. Select rule
2. Click **🗑️ Delete**
3. Confirm

#### 4. Logs Tab

- View routing logs
- View application logs
- Click **🔄 Refresh** to update

### Header Controls

- **▶ Start**: Start email router (continuous mode)
- **⏸ Stop**: Stop email router
- **Status Indicator**: 
  - 🟢 Green = Running
  - 🔴 Red = Stopped

### Tips

1. **First Time Use**: 
   - Go to Configuration tab and set all settings
   - Add rules in Rules tab
   - Then click Start

2. **Rules Management**:
   - Rules can be added/edited/deleted anytime
   - No need to restart router after rule changes

3. **Configuration**:
   - Must restart router after configuration changes

4. **Logs**:
   - View all activity in Logs tab
   - Both routing history and application logs available

---

## Routing Rules / রাউটিং রুলস {#routing-rules}

### Creating Rules

#### Method 1: Using GUI (Easiest)

1. Open GUI
2. Go to Rules tab
3. Click **➕ Add Rule**
4. Use Quick Rule for simple forwarding or Advanced Rule for complex conditions

#### Method 2: Using CLI Tool

```bash
python3 manage_rules.py
```

Menu options:
- **1** - List all rules
- **2** - Add new rule
- **3** - Enable rule
- **4** - Disable rule
- **5** - Edit rule
- **6** - Delete rule
- **7** - View routing logs

#### Method 3: Direct YAML Editing

Edit `routing_rules.yaml`:

```yaml
rules:
  - name: "Fire Insurance - RRR Insurance"
    enabled: true
    match_type: "any"
    conditions:
      subject_keywords:
        - "fire insurance"
        - "অগ্নি বীমা"
      body_keywords:
        - "RRR"
    forward_to:
      - "rrr.insurance@example.com"
```

### Rule Structure

#### **name**: Rule name
Any descriptive name you prefer

#### **enabled**: Enable/Disable
- `true` = Rule is active
- `false` = Rule is disabled

#### **match_type**: Matching type
- `any` = Match if ANY condition is met
- `all` = Match if ALL conditions are met

#### **conditions**: Matching conditions

**subject_keywords**: Match if subject contains these words
```yaml
subject_keywords:
  - "fire insurance"
  - "marine insurance"
```

**body_keywords**: Match if body contains these words
```yaml
body_keywords:
  - "RRR"
  - "insurance claim"
```

**from_contains**: Match if sender email contains these patterns
```yaml
from_contains:
  - "specific.person@yourcompany.com"
```

**subject_regex**: Advanced pattern matching (Regex)
```yaml
subject_regex: "Policy.*RRR-\\d+"
```

#### **forward_to**: Recipient emails
```yaml
forward_to:
  - "insurance1@example.com"
  - "insurance2@example.com"  # Multiple recipients
```

### Rule Examples

#### Example 1: Simple Keyword Matching

```yaml
- name: "Marine Insurance - ZZZ Company"
  enabled: true
  match_type: "any"
  conditions:
    subject_keywords:
      - "marine insurance"
      - "সামুদ্রিক বীমা"
      - "cargo"
  forward_to:
    - "zzz.insurance@example.com"
```

#### Example 2: Multiple Conditions (ALL must match)

```yaml
- name: "Specific Person - Fire Insurance"
  enabled: true
  match_type: "all"  # All conditions must match
  conditions:
    from_contains:
      - "john.doe@yourcompany.com"
    subject_keywords:
      - "fire insurance"
  forward_to:
    - "special.insurance@example.com"
```

#### Example 3: Multiple Recipients

```yaml
- name: "Health Insurance - All Companies"
  enabled: true
  match_type: "any"
  conditions:
    subject_keywords:
      - "health insurance"
      - "medical insurance"
  forward_to:
    - "health1@insurance.com"
    - "health2@insurance.com"
    - "health3@insurance.com"
```

#### Example 4: Regex Pattern Matching

```yaml
- name: "Policy Number Based Routing"
  enabled: true
  match_type: "any"
  conditions:
    subject_regex: "Policy.*ABC-\\d{4,6}"
  forward_to:
    - "abc.insurance@example.com"
```

### Default Rule

If no rule matches, default rule will be used:

```yaml
default_rule:
  enabled: true
  name: "Default - All Insurance"
  forward_to:
    - "general@insurance1.com"
    - "general@insurance2.com"
```

---

## Running the System / সিস্টেম চালু করা {#running}

### Test Mode (Run Once)

```bash
# Virtual environment activate
source venv/bin/activate    # Linux/Mac
venv\Scripts\activate.bat   # Windows

# Run once
python3 email_router.py --once
```

### Continuous Mode

```bash
# Default: check every 60 seconds
python3 email_router.py

# Custom interval: check every 30 seconds
python3 email_router.py --interval 30

# Custom interval: check every 5 minutes
python3 email_router.py --interval 300
```

### Using GUI

1. Start GUI: `run_gui.bat` or `./run_gui.sh`
2. Configure settings in Configuration tab
3. Add rules in Rules tab
4. Click **▶ Start** button

### Background Execution

#### Linux/Mac

**Using screen:**
```bash
screen -S email_router
source venv/bin/activate
python3 email_router.py
# Press Ctrl+A, D to detach

# To reattach:
screen -r email_router
```

**Using nohup:**
```bash
nohup python3 email_router.py > email_router_output.log 2>&1 &
```

**Using systemd service:**
```bash
sudo nano /etc/systemd/system/email-router.service
```

```ini
[Unit]
Description=Email Routing Service
After=network.target

[Service]
Type=simple
User=your-username
WorkingDirectory=/path/to/email-router
ExecStart=/path/to/venv/bin/python3 email_router.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable email-router
sudo systemctl start email-router
sudo systemctl status email-router
```

#### Windows

**Using Task Scheduler:**
1. Open Task Scheduler
2. Create Basic Task
3. Set trigger (At startup or At log on)
4. Action: Start a program
   - Program: `C:\path\to\venv\Scripts\pythonw.exe`
   - Arguments: `email_router.py`
   - Start in: `C:\path\to\project`

**Or simply:**
- Run `python email_router.py`
- Minimize the window

---

## Project Structure / প্রকল্পের গঠন {#project-structure}

### Core Files

```
.
├── email_router.py           # Main email routing script
├── gui_app.py                # GUI application
├── manage_rules.py           # CLI tool for managing rules
├── test_setup.py             # Setup validation script
│
├── config.yaml               # Email configuration (EDIT THIS)
├── routing_rules.yaml         # Routing rules (EDIT THIS)
├── example_config.yaml        # Example configuration template
│
├── setup.sh                  # Setup script (Linux/Mac)
├── setup.bat                 # Setup script (Windows)
├── run_gui.sh                # GUI launcher (Linux/Mac)
├── run_gui.bat               # GUI launcher (Windows)
├── requirements.txt          # Python dependencies
│
├── email_router.log          # Application log (auto-generated)
├── routing_log.json          # Routing history (auto-generated)
├── processed_emails.txt      # Processed email IDs (auto-generated)
├── failed_emails.txt         # Failed email IDs (auto-generated)
│
└── DOCUMENTATION.md          # This file (complete documentation)
```

### Workflow

```
1. SETUP
   └─> Run setup.sh or setup.bat
       └─> Creates virtual environment
       └─> Installs dependencies

2. CONFIGURATION
   └─> Edit config.yaml
       └─> Add email credentials
       └─> Add department emails
   └─> Edit routing_rules.yaml
       └─> Add routing rules
       └─> OR use GUI or manage_rules.py

3. VALIDATION
   └─> Run test_setup.py
       └─> Checks all configuration
       └─> Tests email connection

4. EXECUTION
   └─> Run email_router.py or GUI
       └─> Monitors inbox
       └─> Applies routing rules
       └─> Forwards emails
       └─> Logs actions

5. MONITORING
   └─> Check email_router.log
   └─> Check routing_log.json
   └─> View logs in GUI
```

---

## Alternative Solutions / বিকল্প সমাধান {#alternatives}

If you don't want to keep your PC on 24/7, here are alternative solutions:

### 1. Google Apps Script (Completely Free ⭐ Most Convenient)

**Advantages:**
- ✅ Completely free
- ✅ No PC needs to be on
- ✅ Runs on Google's servers
- ✅ Directly integrated with Gmail
- ✅ Easy setup

**Disadvantages:**
- ⚠️ Only for Gmail
- ⚠️ Limited execution time (6 minutes/execution per day)

### 2. Cloud VPS/Server (Professional Solution)

**Services:**

#### a) DigitalOcean Droplet
- **Price:** $4-6/month (Basic Droplet)
- **Advantage:** Runs 24/7, full control
- **Link:** https://www.digitalocean.com/

#### b) AWS EC2 (Free Tier)
- **Price:** Free for first 1 year (750 hours/month)
- **Advantage:** Amazon's reliable service
- **Link:** https://aws.amazon.com/free/

#### c) Google Cloud (Free Tier)
- **Price:** $300 credit for first 90 days
- **Advantage:** Google's infrastructure
- **Link:** https://cloud.google.com/free

#### d) Heroku (Easy)
- **Price:** $5-7/month
- **Advantage:** Very easy deployment
- **Link:** https://www.heroku.com/

#### e) PythonAnywhere
- **Price:** Starting from $5/month
- **Advantage:** Specifically designed for Python
- **Link:** https://www.pythonanywhere.com/

**Setup Process:**
1. Buy VPS
2. Install Ubuntu/Linux
3. Upload the scripts
4. Start systemd service
5. Runs 24/7!

### 3. Raspberry Pi (One-time Cost, Always Running)

**Advantages:**
- ✅ Buy once (~$35-50)
- ✅ Very low power consumption (~3-5W)
- ✅ Can run 24/7
- ✅ Almost no monthly cost
- ✅ At home under your control

**Requirements:**
- Raspberry Pi 4 (2GB RAM or more)
- MicroSD Card (16GB+)
- Power Supply
- Internet connection

**Monthly Power Cost:**
- Approximately 30-50 Taka (even if running all day!)

### 4. Old Laptop/PC as Server

**Advantages:**
- ✅ No new cost
- ✅ Can use any old laptop/PC
- ✅ Full control

**Tips:**
- Install lightweight Linux (Ubuntu Server)
- Turn off display/monitor
- Enable power saving mode
- Set up in a corner

**Power Cost:**
- Old laptop: ~200-400 Taka/month
- Old desktop: ~500-1000 Taka/month

### Comparison Table

| Solution | Initial Cost | Monthly Cost | Advantages | Disadvantages |
|----------|-------------|--------------|------------|---------------|
| **Google Apps Script** | Free | Free | Completely free, easy | Only Gmail |
| **AWS Free Tier** | Free | Free (1 year) | Professional | Complex setup |
| **DigitalOcean** | Free | $6 | Easy, reliable | Monthly cost |
| **Raspberry Pi** | $50 | ~৳50 | One-time cost | Need to buy hardware |
| **Old Laptop** | Free | ~৳300 | No cost | Higher power consumption |
| **PythonAnywhere** | Free | $5 | Python ready | Limited resources |

---

## Update History / আপডেটের ইতিহাস {#updates}

### Latest Updates

#### Version 2.0 - GUI Application
- ✅ Modern GUI interface with Tkinter
- ✅ Dashboard with statistics
- ✅ Configuration management through GUI
- ✅ Rules management with Quick Rule and Advanced Rule
- ✅ Real-time logs viewing
- ✅ Start/Stop controls
- ✅ Failed emails tracking and retry
- ✅ Email provider auto-detection
- ✅ Password helper (auto-removes spaces)
- ✅ Modern UI design with gradient colors
- ✅ Card-based layout
- ✅ English-only UI (Bengali text removed from interface)

#### Version 1.5 - SMTP SSL/TLS Support
- ✅ Port 465 SSL/TLS support
- ✅ Port 587 STARTTLS support
- ✅ Auto-detection of connection method
- ✅ Custom domain support improved

#### Version 1.4 - Failed Email Retry
- ✅ Failed email tracking (`failed_emails.txt`)
- ✅ Automatic retry mechanism
- ✅ Manual retry option in GUI
- ✅ Emails only marked as read after successful forward

#### Version 1.3 - Quick Rule Feature
- ✅ Quick Rule creation in GUI
- ✅ One-click forwarding from Commercial to Insurance Department
- ✅ Auto-generated rule names

#### Version 1.2 - Email Provider Auto-Detection
- ✅ Gmail auto-detection
- ✅ Outlook/Office365 auto-detection
- ✅ Yahoo auto-detection
- ✅ Custom domain auto-detection
- ✅ Auto-fill settings button

#### Version 1.1 - Password Handling
- ✅ App Password space removal
- ✅ Helper button for password formatting
- ✅ Auto-format on save

#### Version 1.0 - Initial Release
- ✅ Basic email routing
- ✅ Rule-based forwarding
- ✅ CLI tool for rule management
- ✅ Logging system
- ✅ Bengali keyword support

---

## Troubleshooting / সমস্যা সমাধান {#troubleshooting}

### Problem: Authentication Failed

**Solution:**
- For Gmail: Use App Password, not regular password
- Enable 2-Step Verification
- Check username and password are correct
- Verify IMAP/SMTP server settings

### Problem: Emails Not Forwarding

**Check:**
1. Check `email_router.log` for errors
2. Verify rules are enabled (use GUI or `manage_rules.py`)
3. Check Commercial Department email is correct in `config.yaml`
4. Test with `--once` flag
5. Check if email matches rule conditions

### Problem: SMTP Connection Failed (Port 465)

**Solution:**
- Port 465 uses SSL/TLS directly
- Make sure you're using `smtplib.SMTP_SSL` (system handles this automatically)
- Check firewall settings
- Verify SMTP server and port are correct

### Problem: GUI Not Starting

**Check:**
1. Python 3.7+ installed?
2. Virtual environment activated?
3. Dependencies installed? Run `pip install -r requirements.txt`
4. Tkinter installed? (usually comes with Python)

### Problem: Configuration Not Saving

**Check:**
1. File permissions
2. Error message in GUI
3. Check if `config.yaml` is writable

### Problem: Router Not Starting

**Check:**
1. Configuration file (`config.yaml`) exists?
2. Email settings correct?
3. Gmail App Password being used?
4. Check logs for specific error messages

### Problem: Rules Not Updating

**Solution:**
- Rules update automatically on next email check
- No need to restart router for rule changes
- Only restart if `config.yaml` is modified

### Problem: "No module named 'yaml'"

**Solution:**
```bash
pip install PyYAML
```

Or activate virtual environment:
```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.bat  # Windows
```

---

## FAQ / প্রশ্নোত্তর {#faq}

### Q: Can I forward the same email to multiple insurance companies?

**A:** Yes, add multiple emails to `forward_to`:
```yaml
forward_to:
  - "insurance1@example.com"
  - "insurance2@example.com"
  - "insurance3@example.com"
```

### Q: Can I use Bengali keywords?

**A:** Yes, full Bengali support:
```yaml
subject_keywords:
  - "অগ্নি বীমা"
  - "সামুদ্রিক বীমা"
```

### Q: What happens to emails not from Commercial Department?

**A:** Only emails from addresses listed in `commercial_department.emails` in `config.yaml` are processed. All others are ignored.

### Q: How do I know if an email was forwarded?

**A:** 
- Check `email_router.log`
- Use GUI Logs tab
- Run `python3 manage_rules.py` and select option 7
- Check `routing_log.json` file

### Q: Will it start automatically after server restart?

**A:** Linux: Set up systemd service (see Running section). Windows: Use Task Scheduler.

### Q: Can I use custom domain emails (e.g., rony@epagebd.com)?

**A:** Yes! The system supports:
- Gmail
- Outlook/Office365
- Yahoo
- Custom domains (e.g., epagebd.com)

Use GUI's Auto-Fill Settings button for automatic configuration.

### Q: What ports should I use?

**A:**
- **IMAP:** Usually 993 (SSL)
- **SMTP:** 
  - Port 465 = SSL/TLS (most custom domains)
  - Port 587 = STARTTLS (Gmail, Outlook)

The system automatically detects and uses the correct method.

### Q: What if an email fails to forward?

**A:** The system:
- Saves failed email ID to `failed_emails.txt`
- Retries automatically on next run
- Can be manually retried using GUI "Retry Failed" button
- Email remains unread until successfully forwarded

### Q: How often does it check for emails?

**A:** Default is 60 seconds. Can be changed:
- In `config.yaml`: `check_interval: 60`
- Via GUI: Configuration tab → Check Interval
- Via CLI: `python3 email_router.py --interval 30`

### Q: Can I run it without GUI?

**A:** Yes! Use CLI:
```bash
python3 email_router.py
```

---

## Logging and Monitoring / লগিং এবং মনিটরিং

### Log Files

1. **email_router.log** - Main activity log
2. **routing_log.json** - Detailed routing history
3. **processed_emails.txt** - List of processed email IDs
4. **failed_emails.txt** - List of failed email IDs (with retry info)

### View Logs

**Using GUI:**
- Go to **Logs** tab
- Click **🔄 Refresh** to update

**Using CLI:**
```bash
# Real-time log monitoring
tail -f email_router.log

# View routing history
python3 manage_rules.py
# Select option 7
```

---

## Security Best Practices / নিরাপত্তার সেরা অনুশীলন

1. **Use App Passwords**, not account passwords
2. **Never commit** `config.yaml` to version control
3. **Set proper file permissions:**
   ```bash
   chmod 600 config.yaml
   ```
4. **Add to `.gitignore`:**
   ```
   config.yaml
   processed_emails.txt
   routing_log.json
   email_router.log
   failed_emails.txt
   ```
5. **Regularly review** routing logs
6. **Use secure connections** (SSL/TLS)
7. **Keep Python and dependencies updated**

---

## Requirements / প্রয়োজনীয়তা

- **Python 3.7 or higher**
- **Internet connection**
- **Email account with IMAP/SMTP access**

### Dependencies

- **PyYAML** - YAML configuration parsing
- **python-dateutil** - Date/time handling
- **email-validator** - Email validation
- **Standard library modules** (imaplib, smtplib, email, tkinter)

Install all:
```bash
pip install -r requirements.txt
```

---

## Support / সাহায্য

For issues and questions:
1. Check log files (`email_router.log`)
2. Review configuration (`config.yaml`, `routing_rules.yaml`)
3. Run in test mode: `python3 email_router.py --once`
4. Use GUI for easier management
5. Check this documentation

---

## License / লাইসেন্স

This software is free and open source.

---

**Happy Email Routing! 🚀**

**শুভ ইমেইল রাউটিং! 🎉**

---

*Last Updated: November 2024*  
*Last Modified: GUI v2.0 - Modern Interface with English-only UI*

