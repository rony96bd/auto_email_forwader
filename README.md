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

### 2. Configure
Edit `config.yaml` with your email settings.

### 3. Run GUI
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

---

## 📝 License

Free and open source.

---

**For detailed documentation, see [DOCUMENTATION.md](DOCUMENTATION.md)**

**Happy Email Routing! 🚀**

