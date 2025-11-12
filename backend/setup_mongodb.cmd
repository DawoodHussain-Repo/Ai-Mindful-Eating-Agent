@echo off
echo ========================================
echo MongoDB Setup for Mindful Eating App
echo ========================================
echo.

echo Checking MongoDB connection...
mongosh --eval "db.version()" --quiet >nul 2>&1

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] MongoDB is not running or not installed!
    echo.
    echo Please ensure:
    echo 1. MongoDB is installed on your system
    echo 2. MongoDB service is running
    echo 3. MongoDB is accessible on localhost:27017
    echo.
    echo To start MongoDB:
    echo - Windows: net start MongoDB
    echo - Or run: mongod
    echo.
    pause
    exit /b 1
)

echo [OK] MongoDB is running!
echo.

echo Creating database and collections...
mongosh mindful_eating_db --eval "db.createCollection('users'); db.createCollection('food_logs'); db.createCollection('sessions'); print('Collections created successfully!');" --quiet

echo.
echo Creating indexes...
mongosh mindful_eating_db --eval "db.users.createIndex({email: 1}, {unique: true}); db.food_logs.createIndex({user_id: 1}); db.food_logs.createIndex({timestamp: 1}); db.sessions.createIndex({session_id: 1}, {unique: true}); print('Indexes created successfully!');" --quiet

echo.
echo ========================================
echo MongoDB setup completed successfully!
echo ========================================
echo.
echo Database: mindful_eating_db
echo Collections: users, food_logs, sessions
echo.
pause
