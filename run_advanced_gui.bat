@echo off
echo ===============================================
echo Image-to-PDF Organizer Pro (PyQt5)
echo ===============================================
echo.

REM Check if we have a Python virtual environment
if exist .venv\Scripts\python.exe (
    echo Using Python virtual environment...
    .venv\Scripts\python.exe -m src.main --qt
) else if exist venv\Scripts\python.exe (
    echo Using Python virtual environment (venv)...
    venv\Scripts\python.exe -m src.main --qt
) else (
    echo Using system Python...
    python -m src.main --qt
)

if errorlevel 1 (
    echo.
    echo Application closed with an error.
    echo.
    echo If PyQt5 is not installed, please run:
    echo pip install PyQt5
    echo.
    echo Or run install_windows.bat to set up everything automatically.
)

pause
