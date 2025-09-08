@echo off
echo ===============================================
echo Image-to-PDF Organizer
echo ===============================================
echo.

REM Check if we have a Python virtual environment
if exist .venv\Scripts\python.exe (
    echo Using Python virtual environment...
    .venv\Scripts\python.exe -m src.main --gui
) else if exist venv\Scripts\python.exe (
    echo Using Python virtual environment (venv)...
    venv\Scripts\python.exe -m src.main --gui
) else (
    echo Using system Python...
    python -m src.main --gui
)

if errorlevel 1 (
    echo.
    echo Application closed with an error.
    echo.
    echo If you haven't installed the required packages, please run:
    echo pip install -r requirements.txt
    echo.
    echo Or run install_windows.bat to set up everything automatically.
)

pause
