@echo off
REM Mindful Eating Agent - Startup Script for Windows
REM This script creates venv, installs dependencies, and starts the Flask app

echo ============================================================
echo   Mindful Eating Agent - Backend Setup and Start
echo ============================================================
echo.

REM Check if Python 3.9 is installed
python3.9 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.9 is not installed or not in PATH
    echo ChromaDB requires Python 3.9-3.12 ^(not 3.13+^)
    echo Please install Python 3.9 from https://www.python.org/
    pause
    exit /b 1
)

echo [1/5] Checking Python version...
python3.9 --version

REM Check if .env file exists
echo.
echo [2/5] Checking configuration...
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please create a .env file with your Gemini API key
    echo.
    echo Required variables:
    echo   CHROMA_USE_LOCAL=true
    echo   GEMINI_API_KEY=your_gemini_key
    pause
    exit /b 1
)
echo [SUCCESS] Configuration file found!

REM Check if venv39 exists
if not exist "venv39" (
    echo.
    echo [3/5] Creating Python 3.9 virtual environment...
    python3.9 -m venv venv39
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created successfully!
) else (
    echo.
    echo [3/5] Virtual environment already exists, skipping creation...
)

REM Activate virtual environment
echo.
echo [4/5] Activating virtual environment...
call venv39\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install/Update requirements
echo.
echo [5/5] Installing/Updating dependencies...
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
