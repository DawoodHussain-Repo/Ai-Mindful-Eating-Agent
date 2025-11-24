@echo off
echo ============================================================
echo   Mindful Eating Agent - Flask Application Startup
echo ============================================================
echo.

REM Check Python 3.9
python3.9 --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.9 is not installed or not in PATH
    echo ChromaDB requires Python 3.9-3.12 ^(not 3.13+^)
    echo Please install Python 3.9 from https://www.python.org/
    pause
    exit /b 1
)
echo [OK] Python 3.9 is installed

REM Check .env file
echo.
echo [1/4] Checking configuration...
if not exist "backend\.env" (
    echo [ERROR] .env file not found in backend directory!
    echo Please create backend\.env with your Gemini API key
    pause
    exit /b 1
)
echo [OK] Configuration file found

REM Setup Backend if needed
echo.
echo [2/4] Setting up Backend...
if not exist "backend\venv39" (
    echo Creating Python 3.9 virtual environment...
    cd backend
    python3.9 -m venv venv39
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)

REM Install/Update Backend Dependencies
echo.
echo [3/4] Installing/Updating backend dependencies...
cd backend
echo Activating virtual environment...
call .\venv39\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment
    cd ..
    pause
    exit /b 1
)
echo Upgrading pip...
.\venv39\Scripts\python.exe -m pip install --upgrade pip >nul 2>&1
echo Installing dependencies from requirements.txt...
.\venv39\Scripts\python.exe -m pip install -r requirements.txt
if errorlevel 1 (
    echo [WARNING] Some dependencies may have failed to install
    echo Please check the error messages above
)
cd ..
echo [OK] Backend setup complete

REM Start Flask Application
echo.
echo [4/4] Starting Flask Application...
start "Mindful Eating Agent - Flask Server" cmd /k "cd /d "%~dp0backend" && .\venv39\Scripts\python.exe app.py"

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
echo Database:        ChromaDB ^(Local Storage^)
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
