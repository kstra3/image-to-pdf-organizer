@echo off
echo ====================================
echo   Image-to-PDF Organizer GUI
echo ====================================
echo.
echo Choose your interface:
echo 1. Advanced PyQt5 GUI (Recommended)
echo 2. Basic Tkinter GUI
echo 3. Auto-detect best GUI
echo.
set /p choice="Enter your choice (1-3): "

cd /d "%~dp0"

if "%choice%"=="1" (
    echo.
    echo Starting Advanced PyQt5 GUI...
    python main.py --gui pyqt5
) else if "%choice%"=="2" (
    echo.
    echo Starting Basic Tkinter GUI...
    python main.py --gui tkinter
) else if "%choice%"=="3" (
    echo.
    echo Auto-detecting best GUI...
    python main.py --gui auto
) else (
    echo.
    echo Invalid choice. Starting auto-detection...
    python main.py --gui auto
)

if errorlevel 1 (
    echo.
    echo Error: Could not start GUI
    echo Make sure you have installed requirements:
    echo pip install -r requirements.txt
    echo.
)

echo.
echo GUI closed. Press any key to exit...
pause >nul
