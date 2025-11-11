@echo off
REM Mindful Eating Agent - Run Only Script
REM This script assumes venv is already set up and just runs the app

echo ============================================================
echo   Mindful Eating Agent - Starting Application
echo ============================================================
echo.

REM Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment not found!
    echo Please run setup.cmd first to create the environment.
    pause
    exit /b 1
)

REM Activate venv and run app
call venv\Scripts\activate.bat
echo Server starting on: http://localhost:5000
echo Press CTRL+C to stop the server
echo.
python app.py

deactivate
