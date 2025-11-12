@echo off
echo ============================================================
echo   Mindful Eating Agent - Full Stack Startup
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

REM Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18 or higher from https://nodejs.org/
    pause
    exit /b 1
)

REM Check MongoDB
echo [1/6] Checking MongoDB...
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
echo [2/6] Setting up Backend...
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
pip install -r requirements.txt >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
)
cd ..
echo [OK] Backend setup complete

REM Setup Frontend if needed
echo.
echo [3/6] Setting up Frontend...
if not exist "frontend\node_modules" (
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
    cd ..
)
echo [OK] Frontend setup complete

REM Start Backend
echo.
echo [4/6] Starting Flask Backend...
start "Mindful Eating - Backend" cmd /k "cd backend && call venv\Scripts\activate.bat && python app.py"

REM Wait for backend to start
echo Waiting for backend to initialize...
timeout /t 8 /nobreak >nul

REM Start Frontend
echo.
echo [5/6] Starting Next.js Frontend...
start "Mindful Eating - Frontend" cmd /k "cd frontend && npm run dev"

REM Wait and open browser
echo.
echo [6/6] Opening browser...
timeout /t 10 /nobreak >nul
start http://localhost:3000

echo.
echo ============================================================
echo   Full Stack Running Successfully!
echo ============================================================
echo.
echo Backend API:  http://localhost:5000
echo Frontend App: http://localhost:3000
echo MongoDB:      localhost:27017
echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this window...
pause >nul
