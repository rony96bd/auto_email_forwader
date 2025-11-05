@echo off
REM Email Router GUI Launcher for Windows

echo Starting Email Router GUI...

cd /d "%~dp0"

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)

REM Run the GUI application
python gui_app.py

pause

