@echo off
title Image-to-PDF Organizer - Smart Launcher
color 0A

echo.
echo  ██╗███╗   ███╗ ██████╗    ████████╗ ██████╗     ██████╗ ██████╗ ███████╗
echo  ██║████╗ ████║██╔════╝    ╚══██╔══╝██╔═══██╗    ██╔══██╗██╔══██╗██╔════╝
echo  ██║██╔████╔██║██║  ███╗      ██║   ██║   ██║    ██████╔╝██║  ██║█████╗  
echo  ██║██║╚██╔╝██║██║   ██║      ██║   ██║   ██║    ██╔═══╝ ██║  ██║██╔══╝  
echo  ██║██║ ╚═╝ ██║╚██████╔╝      ██║   ╚██████╔╝    ██║     ██████╔╝██║     
echo  ╚═╝╚═╝     ╚═╝ ╚═════╝       ╚═╝    ╚═════╝     ╚═╝     ╚═════╝ ╚═╝     
echo.
echo                          ORGANIZER PRO v2.0
echo  ========================================================================
echo.

REM Check for Python environment
if exist .venv\Scripts\python.exe (
    set PYTHON_EXE=.venv\Scripts\python.exe
    echo  ✅ Virtual environment detected
) else if exist venv\Scripts\python.exe (
    set PYTHON_EXE=venv\Scripts\python.exe
    echo  ✅ Virtual environment detected
) else (
    set PYTHON_EXE=python
    echo  ⚠️  Using system Python
)

echo.
echo  🚀 LAUNCH OPTIONS:
echo  ==================
echo.
echo  [1] 🎨 Advanced GUI (PyQt5) - Dark theme, drag-drop, thumbnails
echo  [2] 🖼️  Basic GUI (Tkinter) - Simple, lightweight interface
echo  [3] 💻 Command Line - For batch processing
echo  [4] 🛠️  Smart Auto-Select - Let the app choose the best GUI
echo  [5] ❌ Exit
echo.

set /p choice="  Enter your choice (1-5): "

if "%choice%"=="1" goto advanced_gui
if "%choice%"=="2" goto basic_gui
if "%choice%"=="3" goto cli_help
if "%choice%"=="4" goto auto_select
if "%choice%"=="5" goto exit
echo  ❌ Invalid choice. Please try again.
pause
goto :EOF

:advanced_gui
echo.
echo  🎨 Starting Advanced PyQt5 GUI...
echo  ====================================
%PYTHON_EXE% -m src.main --qt
goto end

:basic_gui
echo.
echo  🖼️  Starting Basic Tkinter GUI...
echo  =================================
%PYTHON_EXE% -m src.main --gui tkinter
goto end

:cli_help
echo.
echo  💻 Command Line Interface
echo  =========================
echo.
echo  Usage examples:
echo  %PYTHON_EXE% -m src.main image1.jpg image2.png -o output.pdf
echo  %PYTHON_EXE% -m src.main *.jpg -o photos.pdf -s A4 -c -q 80
echo.
echo  Options:
echo    -o, --output       Output PDF file path
echo    -s, --page-size    Page size (A4, LETTER, LEGAL, TABLOID, FIT)
echo    -c, --compress     Enable compression
echo    -q, --quality      Compression quality (1-100)
echo.
echo  For more help: %PYTHON_EXE% -m src.main --help
echo.
pause
goto :EOF

:auto_select
echo.
echo  🛠️  Auto-selecting best GUI...
echo  ===============================
%PYTHON_EXE% -m src.launcher
goto end

:exit
echo.
echo  👋 Goodbye!
exit /b 0

:end
if errorlevel 1 (
    echo.
    echo  ❌ Application encountered an error.
    echo.
    echo  💡 Troubleshooting tips:
    echo     - Make sure all dependencies are installed: pip install -r requirements.txt
    echo     - For PyQt5 issues, try: pip uninstall PyQt5 ^&^& pip install PyQt5
    echo     - Check if your Python installation includes tkinter
    echo.
)
pause
