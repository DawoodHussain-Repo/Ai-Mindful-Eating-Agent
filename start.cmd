@echo off
REM Mindful Eating Agent - Quick Start Script
REM This script navigates to backend and runs the startup script

echo ============================================================
echo   Mindful Eating Agent - Quick Start
echo ============================================================
echo.

REM Navigate to backend directory
cd backend

REM Run the backend start script
call start.cmd

REM Return to root directory
cd ..
