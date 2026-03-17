@echo off
setlocal

:: Check for Python
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.10 or newer from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check Python version is 3.10+
python -c "import sys; exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 (
    echo Python 3.10 or newer is required. Please update your Python installation.
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
set VENV_DIR=%~dp0.venv
if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo Creating virtual environment...
    python -m venv "%VENV_DIR%"
)

:: Activate virtual environment
call "%VENV_DIR%\Scripts\activate.bat"

:: Check and install dependencies inside venv
echo Checking dependencies...
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo Installing PySide6...
    python -m pip install PySide6
)

python -c "import openpyxl" >nul 2>&1
if errorlevel 1 (
    echo Installing openpyxl...
    python -m pip install openpyxl
)

:: Launch the app
set PYTHONPATH=%~dp0src
python -m degreeplaner.CurriculumPlaner

endlocal
