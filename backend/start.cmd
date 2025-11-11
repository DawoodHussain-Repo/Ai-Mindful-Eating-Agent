@echo off
REM Mindful Eating Agent - Startup Script for Windows
REM This script creates venv, installs dependencies, and starts the Flask app

echo ============================================================
echo   Mindful Eating Agent - Backend Setup and Start
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

echo [1/4] Checking Python version...
python --version

REM Check if venv exists
if not exist "venv" (
    echo.
    echo [2/4] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully!
) else (
    echo.
    echo [2/4] Virtual environment already exists, skipping creation...
)

REM Activate virtual environment
echo.
echo [3/4] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/Update requirements
echo.
echo [4/4] Installing/Updating dependencies...
echo This may take a few minutes on first run...
python -m pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install requirements
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   Setup Complete! Starting Flask Application...
echo ============================================================
echo.
echo Server will start on: http://localhost:5000
echo Press CTRL+C to stop the server
echo.

REM Start Flask app
python app.py

REM Deactivate venv when app stops
deactivate
