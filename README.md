# Mindful Eating Agent

<div align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Flask-3.0-green" alt="Flask 3.0">
  <img src="https://img.shields.io/badge/MongoDB-6.0%2B-brightgreen" alt="MongoDB 6.0+">
  <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License: MIT">
</div>

## Overview

Mindful Eating Agent is an AI-powered nutrition tracking application that helps users log meals, track nutrition, and receive personalized recommendations through a conversational interface.
- **Modern Design**: Clean, professional UI with gradients and animations

### Enhanced UX
- **2 Modes**: AI Chat and Manual Dashboard
- **Easy Navigation**: Simple header navigation
- **Real-time Updates**: Instant feedback on logging
- **Mobile Responsive**: Works on all devices
- **Progress Sidebar**: Quick stats while chatting

## API Endpoints

### New Endpoints

**POST** `/api/chat`
- Conversational food logging
- Handles natural language input
- Returns AI response and parsed foods

**GET** `/api/calendar-logs?days=30`
- Get historical logs organized by date
- Returns daily summaries and meal details

### Existing Endpoints

**POST** `/register` - Create account with custom goals  
**POST** `/login` - Authenticate user  
**GET** `/logout` - End session  
**POST** `/api/log-food` - Manual food logging  
**GET** `/api/get-logs` - Get today's logs  
**GET** `/api/get-recommendations` - Get AI insights  
**GET** `/api/get-stats` - Get user statistics

## Usage Examples

### Chat Interface
```
User: "had a burger and fries"
AI: "Got it! Logged: Burger (1 serving), Fries (1 serving) 📝

📊 Nutrition Summary:
• 666 calories
• 23g protein
• 71g carbs
• 25g fat

🔥 That's a solid meal!"

[AI Insights appear below]
✨ AI Insights
💪 You're at 85g protein today (goal: 120g). Try adding some chicken or Greek yogurt!
```

### Misspelling Handling
```
User: "ate chiken and ryce"
AI: "Did you mean 'Chicken', 'Rice'? 🤔
(Reply 'yes' to confirm or tell me what you actually meant)"
User: "yes"
AI: "Perfect! Logged: Chicken (1 serving), Rice (1 serving) ✅"
```

### Dashboard
- Manual food logging with meal type selection
- Real-time progress bars for calories and protein
- Today's meal history with nutrition breakdown
- AI recommendations based on patterns

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Architecture](docs/ARCHITECTURE.md)** - System design
- **[API Reference](docs/API.md)** - Endpoint documentation
- **[Spec](Spec.md)** - Technical specification
- **[Workflow](Workflow.md)** - AI agent workflow

## Development

### Running the Application
```bash
cd backend
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
python app.py
```
Runs on: http://localhost:5000

### Available Routes
- `/` - Dashboard (manual logging)
- `/chat` - AI Chat interface
- `/login` - User login
- `/register` - User registration
- `/logout` - Logout

### API Endpoints
All API endpoints are documented in [docs/API.md](docs/API.md)

## Team

- **Gulsher Khan** - Tech Lead
- **Ahsan Faraz** - AI/ML Developer
- **Dawood Hussain** - Project Manager

## License

MIT License
