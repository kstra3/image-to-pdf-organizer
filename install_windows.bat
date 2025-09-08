@echo off
echo ===============================================
echo Installing Image-to-PDF Organizer dependencies
echo ===============================================
echo.

REM Check if Python is installed
python --version 2>NUL
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Create a virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment.
    pause
    exit /b 1
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment.
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo ===============================================
echo Installation complete!
echo.
echo To start the application:
echo - Command line: venv\Scripts\python -m src.main
echo - GUI interface: venv\Scripts\python -m src.main --gui
echo ===============================================
echo.

pause
