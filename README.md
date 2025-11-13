# Email Routing System
# স্বয়ংক্রিয় ইমেইল রাউটিং সিস্টেম

An automated email forwarding system that routes emails from Commercial Department to appropriate insurance companies based on configurable rules.

কমার্শিয়াল ডিপার্টমেন্ট থেকে আসা ইমেইল স্বয়ংক্রিয়ভাবে সঠিক ইন্সুরেন্স কোম্পানিতে পাঠানোর সম্পূর্ণ সমাধান।

---

## 🚀 Quick Start

### 1. Setup
```bash
# Linux/Mac
chmod +x setup.sh && ./setup.sh

# Windows
setup.bat
```

### 2. Activate License
Place your license key into `license.key` (project root) **or** set the `LICENSE_KEY` environment variable.  
You can also host the key at `https://epagebd.com/license.key` (or set `LICENSE_KEY_URL` to your own URL) and the app will fetch it automatically.  
If your licensing endpoint differs from the default, export `LICENSE_SERVER_URL`.

### 3. Configure
Edit `config.yaml` with your email settings.

### 4. Run GUI
```bash
# Windows
run_gui.bat

# Linux/Mac
./run_gui.sh
```

---

## ✨ Features

- ✅ Automatic email forwarding
- ✅ Modern GUI interface
- ✅ Configurable routing rules
- ✅ Multiple conditions (subject, body, sender)
- ✅ Multiple recipients
- ✅ Automatic CC to Accounts Department
- ✅ Comprehensive logging
- ✅ Failed email retry mechanism
- ✅ SMTP SSL/TLS support (Port 465 & 587)
- ✅ Bengali keywords support
- ✅ Email provider auto-detection
- ✅ Online license validation with tamper detection

---

## 📖 Documentation

**Complete documentation available in [DOCUMENTATION.md](DOCUMENTATION.md)**

Includes:
- Quick Start Guide
- Installation Instructions
- Configuration Guide
- GUI User Guide
- Routing Rules Guide
- Alternative Solutions
- Troubleshooting
- FAQ

---

## 📁 Project Files

```
├── email_router.py      # Main routing script
├── gui_app.py          # GUI application
├── manage_rules.py      # CLI rule manager
├── config.yaml          # Configuration (EDIT THIS)
├── routing_rules.yaml   # Routing rules (EDIT THIS)
├── requirements.txt     # Dependencies
└── DOCUMENTATION.md     # Complete documentation
```

---

## 🔧 Requirements

- Python 3.7+
- Internet connection
- Email account with IMAP/SMTP access
- Valid license key issued for this product

---

## 📝 License

Running the software requires an active e-license.  
The application validates the license against the remote licensing service at startup and whenever processing begins.  
If the license is missing, expired, or tampering is detected, the system stops and displays “License Expired”.

---

**For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)**

**Happy Email Routing! 🚀**

