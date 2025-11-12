# Mindful Eating Agent - Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
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

### 2. Setup Backend

```cmd
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
setup_mongodb.cmd
```

### 3. Setup Frontend

```cmd
cd frontend
npm install
```

### 4. Start Application

**Option A: Full Stack (Recommended)**
```cmd
start-fullstack.cmd
```

**Option B: Manual**
```cmd
# Terminal 1 - Backend
cd backend
venv\Scripts\activate
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 5. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:5000

## Configuration

### Backend (.env)
```bash
SECRET_KEY=your-secret-key-here
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:5000
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

### Frontend Build Errors
```cmd
cd frontend
rm -rf .next node_modules
npm install
```

## Production Deployment

### Backend
```cmd
cd backend
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend
```cmd
cd frontend
npm run build
npm start
```

## Support

- Check MongoDB is running on port 27017
- Verify Python virtual environment is activated
- Ensure Node.js dependencies are installed
- Review browser console for frontend errors
- Check Flask logs for backend errors
