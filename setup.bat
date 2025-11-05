@echo off
REM Email Routing System Setup Script for Windows

echo ==========================================
echo Email Routing System Setup
echo ==========================================
echo.

REM Check Python version
echo Checking Python version...
python --version

if %errorlevel% neq 0 (
    echo Error: Python is not installed!
    pause
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo.
echo Installing required packages...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create necessary files
echo.
echo Creating necessary files...
type nul > processed_emails.txt
type nul > routing_log.json

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo Next steps:
echo 1. Edit config.yaml with your email settings
echo.
echo 2. Edit routing_rules.yaml to configure routing rules
echo.
echo 3. Run the GUI application:
echo    run_gui.bat
echo.
echo    Or run the rules manager:
echo    venv\Scripts\activate.bat
echo    python manage_rules.py
echo.
echo 4. Start the email router:
echo    venv\Scripts\activate.bat
echo    python email_router.py
echo.
pause
