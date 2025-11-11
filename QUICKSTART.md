# Quick Start Guide - Mindful Eating Agent

## Prerequisites

- Python 3.10 or higher installed
- Windows OS (for .cmd scripts)

## Installation & Running

### Option 1: Quick Start (Recommended)

From the project root directory, simply run:

```cmd
start.cmd
```

This will:
1. Navigate to the backend directory
2. Create a virtual environment (if needed)
3. Install all dependencies
4. Start the Flask server

### Option 2: Backend Directory

Navigate to the backend folder and run:

```cmd
cd backend
start.cmd
```

### Option 3: Setup First, Then Run

If you want to separate setup from running:

```cmd
cd backend
setup.cmd    # Run once to set up environment
run.cmd      # Run anytime to start the app
```

## Available Scripts

### Root Directory

- **`start.cmd`** - Quick start from root directory

### Backend Directory

- **`start.cmd`** - Complete setup and start (recommended for first run)
- **`setup.cmd`** - Only setup environment and install dependencies
- **`run.cmd`** - Only run the app (assumes setup is done)

## What Each Script Does

### start.cmd (Complete Setup & Start)
1. ✅ Checks Python installation
2. ✅ Creates virtual environment (venv)
3. ✅ Activates virtual environment
4. ✅ Installs/updates all dependencies
5. ✅ Starts Flask server on http://localhost:5000

### setup.cmd (Setup Only)
1. ✅ Checks Python installation
2. ✅ Creates virtual environment (venv)
3. ✅ Installs all dependencies
4. ⏸️ Does NOT start the server

### run.cmd (Run Only)
1. ✅ Activates existing virtual environment
2. ✅ Starts Flask server
3. ⚠️ Requires setup.cmd to be run first

## First Time Setup

1. Open Command Prompt or PowerShell
2. Navigate to project directory:
   ```cmd
   cd "path\to\AI Mindful Agent"
   ```
3. Run the start script:
   ```cmd
   start.cmd
   ```
4. Wait for dependencies to install (first run takes 2-3 minutes)
5. Open browser to http://localhost:5000

## Subsequent Runs

After the first setup, you can use the faster `run.cmd`:

```cmd
cd backend
run.cmd
```

Or just use `start.cmd` which will skip setup if already done.

## Accessing the Application

Once the server starts, open your browser and go to:

```
http://localhost:5000
```

You should see the login page. Create an account to get started!

## Stopping the Server

Press `CTRL+C` in the command prompt window to stop the server.

## Troubleshooting

### "Python is not installed or not in PATH"
- Install Python 3.10+ from https://www.python.org/
- Make sure to check "Add Python to PATH" during installation

### "Failed to create virtual environment"
- Make sure you have write permissions in the directory
- Try running Command Prompt as Administrator

### "Failed to install requirements"
- Check your internet connection
- Try running: `python -m pip install --upgrade pip`
- Then run the setup script again

### Port 5000 already in use
- Another application is using port 5000
- Stop that application or modify `app.py` to use a different port

## Manual Setup (Alternative)

If the scripts don't work, you can set up manually:

```cmd
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

## Project Structure

```
AI Mindful Agent/
├── start.cmd              # Quick start from root
├── backend/
│   ├── start.cmd          # Complete setup & start
│   ├── setup.cmd          # Setup only
│   ├── run.cmd            # Run only
│   ├── app.py             # Flask application
│   ├── agent.py           # LangGraph AI agent
│   ├── requirements.txt   # Python dependencies
│   ├── static/            # CSS, JS files
│   └── templates/         # HTML templates
├── Spec.md                # Technical specification
└── Workflow.md            # How the AI works
```

## Features

- 📝 Text-based food logging
- 🤖 LangGraph AI agent for intelligent processing
- 📊 Real-time nutrition tracking
- 💡 Personalized recommendations
- 🧠 Pattern recognition

## Next Steps

1. Register a new account
2. Log your first meal
3. View your nutrition dashboard
4. Get AI-powered recommendations

Enjoy your mindful eating journey! 🍽️
