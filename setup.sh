#!/bin/bash
# Email Routing System Setup Script

echo "=========================================="
echo "Email Routing System Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed!"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install requirements
echo ""
echo "Installing required packages..."
pip install --upgrade pip
pip install -r requirements.txt

# Make scripts executable
echo ""
echo "Making scripts executable..."
chmod +x email_router.py
chmod +x manage_rules.py

# Create necessary directories and files
echo ""
echo "Creating necessary files..."
touch processed_emails.txt
touch routing_log.json

echo ""
echo "=========================================="
echo "Setup completed successfully!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Edit config.yaml with your email settings"
echo ""
echo "2. Edit routing_rules.yaml to configure routing rules"
echo ""
echo "3. Run the GUI application:"
echo "   ./run_gui.sh"
echo ""
echo "   Or run the rules manager:"
echo "   source venv/bin/activate"
echo "   python3 manage_rules.py"
echo ""
echo "4. Start the email router:"
echo "   source venv/bin/activate"
echo "   python3 email_router.py"
echo ""
