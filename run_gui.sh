#!/bin/bash
# Email Router GUI Launcher for Linux/Mac

echo "Starting Email Router GUI..."

cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi

# Run the GUI application
python3 gui_app.py

