# Mindful Eating Agent

AI-powered nutrition tracking with conversational interface, smart food recognition, and personalized recommendations.

## Features

### 💬 Conversational AI Chat
- Natural language food logging
- Handles misspellings and typos
- Fuzzy matching for unknown foods
- Context-aware responses
- Real-time nutrition feedback

### 📅 Calendar View
- Historical meal tracking
- Daily nutrition summaries
- Expandable meal details
- 30-day history view
- Pattern visualization

### 🎯 Personalized Onboarding
- Custom calorie goals
- Protein targets
- Macro tracking (carbs, fat)
- Flexible goal setting

### 📊 Smart Tracking
- Real-time progress bars
- Daily nutrition totals
- Macro breakdown
- Goal alignment

### 🤖 AI Recommendations
- Pattern-based insights
- Contextual suggestions
- Positive reinforcement
- Behavioral nudges

## Tech Stack

**Frontend**: Next.js 15, TypeScript, Tailwind CSS, shadcn/ui  
**Backend**: Flask 3.0, Python 3.10, LangGraph, LangChain  
**Database**: MongoDB 6.0  
**AI/ML**: Custom NLP, Fuzzy matching, Pattern recognition

## Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB 6.0+

### Installation

```bash
# 1. Setup Backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
setup_mongodb.cmd

# 2. Setup Frontend
cd frontend
npm install

# 3. Start Full Stack
start-fullstack.cmd
```

Access at: **http://localhost:3000**

## Project Structure

```
├── backend/              # Flask API
│   ├── app.py           # Main application
│   ├── agent.py         # Original LangGraph agent
│   ├── agent_chat.py    # Conversational AI agent
│   ├── config/          # Configuration files
│   ├── data/            # Food database
│   └── utils/           # Utilities
├── frontend/            # Next.js app
│   ├── app/            # Pages & routes
│   ├── components/     # UI components
│   │   ├── chat-interface.tsx
│   │   └── calendar-view.tsx
│   └── lib/            # API client
├── docs/               # Documentation
│   ├── SETUP.md       # Setup guide
│   ├── ARCHITECTURE.md # System design
│   └── API.md         # API reference
├── Spec.md            # Technical specification
└── Workflow.md        # System workflow
```

## Key Improvements

### Conversational AI
- **Fuzzy Matching**: Handles misspellings (e.g., "chiken" → "chicken")
- **Intent Detection**: Understands greetings, questions, and food logging
- **Context Awareness**: Remembers conversation history
- **Natural Responses**: Friendly, encouraging feedback

### Calendar View
- **Daily Summaries**: Total calories, protein, carbs, fat per day
- **Expandable Details**: Click to see individual meals
- **Visual Timeline**: Easy-to-scan history
- **Quick Stats**: Meal count and nutrition at a glance

### Enhanced UX
- **3 Modes**: Chat, Manual logging, History
- **Tab Navigation**: Easy switching between modes
- **Real-time Updates**: Instant feedback on logging
- **Mobile Responsive**: Works on all devices

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

📊 Nutrition:
• 666 calories
• 23g protein
• 71g carbs
• 25g fat

🔥 That's a solid meal!"
```

### Misspelling Handling
```
User: "ate chiken and ryce"
AI: "Did you mean 'Chicken', 'Rice'? (Reply 'yes' to confirm)"
User: "yes"
AI: "Perfect! Logged: Chicken (1 serving), Rice (1 serving) ✅"
```

### Calendar View
- Click any day to expand meal details
- See nutrition breakdown per meal
- Track patterns over time

## Documentation

- **[Setup Guide](docs/SETUP.md)** - Installation and configuration
- **[Architecture](docs/ARCHITECTURE.md)** - System design
- **[API Reference](docs/API.md)** - Endpoint documentation
- **[Spec](Spec.md)** - Technical specification
- **[Workflow](Workflow.md)** - AI agent workflow

## Development

### Backend
```bash
cd backend
venv\Scripts\activate
python app.py
```
Runs on: http://localhost:5000

### Frontend
```bash
cd frontend
npm run dev
```
Runs on: http://localhost:3000

## Team

- **Gulsher Khan** - Tech Lead
- **Ahsan Faraz** - AI/ML Developer
- **Dawood Hussain** - Project Manager

## License

MIT License
