@echo off
REM Mindful Eating Agent - Setup Only Script
REM This script only sets up the environment without starting the app

echo ============================================================
echo   Mindful Eating Agent - Environment Setup
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo [1/3] Checking Python version...
python --version

REM Create venv if it doesn't exist
if not exist "venv" (
    echo.
    echo [2/3] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created!
) else (
    echo.
    echo [2/3] Virtual environment already exists!
)

REM Activate and install requirements
echo.
echo [3/3] Installing dependencies...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Setup Complete!
echo ============================================================
echo.
echo To start the application, run: start.cmd
echo Or manually: 
echo   1. venv\Scripts\activate
echo   2. python app.py
echo.
pause
