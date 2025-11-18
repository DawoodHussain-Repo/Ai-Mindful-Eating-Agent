@echo off
echo ============================================================
echo   Mindful Eating Agent - Flask Application Startup
echo ============================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10 or higher from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python is installed

REM Check MongoDB
echo.
echo [1/4] Checking MongoDB...
mongosh --eval "db.version()" --quiet >nul 2>&1
if errorlevel 1 (
    echo [ERROR] MongoDB is not running!
    echo Please start MongoDB first: net start MongoDB
    pause
    exit /b 1
)
echo [OK] MongoDB is running

REM Setup Backend if needed
echo.
echo [2/4] Setting up Backend...
if not exist "backend\venv" (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        cd ..
        pause
        exit /b 1
    )
    cd ..
)

REM Install/Update Backend Dependencies
echo Installing/Updating backend dependencies...
cd backend
call venv\Scripts\activate.bat
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
    echo Please check the error messages above
)
cd ..
echo [OK] Backend setup complete

REM Start Flask Application
echo.
echo [3/4] Starting Flask Application...
start "Mindful Eating Agent - Flask Server" cmd /k "cd backend && call venv\Scripts\activate.bat && python app.py"

REM Wait for Flask to start
echo Waiting for Flask server to initialize...
timeout /t 5 /nobreak >nul

REM Open browser
echo.
echo [4/4] Opening browser...
timeout /t 3 /nobreak >nul
start http://localhost:5000

echo.
echo ============================================================
echo   Flask Application Running Successfully!
echo ============================================================
echo.
echo Application URL: http://localhost:5000
echo MongoDB:         localhost:27017
echo.
echo The Flask server is running in a separate window.
echo Close that window to stop the server.
echo.
echo Features:
echo   - Dashboard: http://localhost:5000/
echo   - AI Chat:   http://localhost:5000/chat
echo   - Login:     http://localhost:5000/login
echo.
echo Press any key to exit this window...
pause >nul
