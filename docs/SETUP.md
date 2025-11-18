# Mindful Eating Agent - Setup Guide

## Prerequisites

- Python 3.10+
- MongoDB 6.0+

## Quick Start

### 1. Install MongoDB

**Windows:**
```cmd
# Download from: https://www.mongodb.com/try/download/community
# Install as Windows Service
# Or use MongoDB Compass: https://www.mongodb.com/try/download/compass
```

Start MongoDB:
```cmd
net start MongoDB
```

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install mongodb

# Mac (Homebrew)
brew install mongodb-community

# Start MongoDB
sudo systemctl start mongod  # Linux
brew services start mongodb-community  # Mac
```

### 2. Setup Backend

```cmd
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
setup_mongodb.cmd  # Windows
# ./setup_mongodb.sh  # Linux/Mac
```

### 3. Start Application

**Option A: Automated (Recommended - Windows)**
```cmd
start-fullstack.cmd
```

**Option B: Manual**
```cmd
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python app.py
```

### 4. Access Application

- Application: http://localhost:5000
- Dashboard: http://localhost:5000/
- AI Chat: http://localhost:5000/chat
- Login: http://localhost:5000/login

## Configuration

### Flask Secret Key (backend/app.py)
The application uses a default secret key for development. For production, set an environment variable:
```bash
# Windows
set SECRET_KEY=your-secret-key-here

# Linux/Mac
export SECRET_KEY=your-secret-key-here
```

### MongoDB (backend/config/mongodb_config.json)
```json
{
  "connection": {
    "host": "localhost",
    "port": 27017,
    "database": "mindful_eating_db"
  }
}
```

## Verification

Check MongoDB connection:
```cmd
cd backend
python check_mongodb.py
```

Expected output:
```
✅ Connected to database: mindful_eating_db

Collections:
  - users: 0 documents
  - food_logs: 0 documents
  - sessions: 0 documents
```

## Troubleshooting

### MongoDB Connection Error
```cmd
# Check if running
sc query MongoDB

# Start service
net start MongoDB
```

### Backend Import Errors
```cmd
cd backend
pip install -r requirements.txt
```

### Port Already in Use
```cmd
# Windows - Find and kill process on port 5000
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## Production Deployment

### Flask Application
```cmd
cd backend
pip install gunicorn  # Linux/Mac
# pip install waitress  # Windows

# Linux/Mac
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# Windows
waitress-serve --port=5000 app:app
```

### Environment Variables
```bash
# Set production secret key
export SECRET_KEY=your-production-secret-key

# Set Flask environment
export FLASK_ENV=production
```

## Application Structure

### Pages
- **Dashboard** (`/`) - Manual food logging with progress tracking
- **AI Chat** (`/chat`) - ChatGPT-style conversational interface
- **Login** (`/login`) - User authentication
- **Register** (`/register`) - New user registration

### Features
- Real-time nutrition tracking
- AI-powered food recognition
- Fuzzy matching for misspellings
- Pattern-based recommendations
- Progress visualization

## Support

- Check MongoDB is running on port 27017
- Verify Python virtual environment is activated
- Review browser console for JavaScript errors
- Check Flask terminal for backend errors
- Ensure all dependencies are installed
