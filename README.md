# Mindful Eating Agent

AI-powered nutrition tracking with conversational interface, smart food recognition, and personalized recommendations using Flask and LangGraph.

## Features

### 💬 ChatGPT-Style AI Chat Interface
- Natural language food logging
- Handles misspellings and typos
- Fuzzy matching for unknown foods
- Context-aware responses
- Real-time nutrition feedback
- Inline AI insights and recommendations
- Scrollable chat history
- Modern, clean UI design

### 📊 Smart Dashboard
- Real-time progress tracking
- Daily nutrition totals
- Macro breakdown visualization
- Goal alignment indicators
- Today's meal history

### 🎯 Personalized Onboarding
- Custom calorie goals
- Protein targets
- Macro tracking (carbs, fat)
- Flexible goal setting

### 🤖 AI Recommendations (LangGraph)
- Pattern-based insights
- Contextual suggestions
- Positive reinforcement
- Behavioral nudges
- Real-time analysis

## Tech Stack

**Frontend**: HTML5, CSS3, JavaScript (Vanilla)  
**Backend**: Flask 3.0, Python 3.10+  
**AI/ML**: LangGraph, LangChain, Custom NLP  
**Database**: MongoDB 6.0+  
**Features**: Fuzzy matching, Pattern recognition, Conversational AI

## Quick Start

### Prerequisites
- Python 3.10+
- MongoDB 6.0+

### Installation

```bash
# 1. Clone the repository
git clone <repository-url>
cd mindful-eating-agent

# 2. Run the startup script (Windows)
start-fullstack.cmd
```

The script will:
- Check Python and MongoDB
- Create virtual environment
- Install dependencies
- Start Flask server
- Open browser automatically

Access at: **http://localhost:5000**

### Manual Setup

```bash
# 1. Setup Backend
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 2. Setup MongoDB
setup_mongodb.cmd  # Windows
# ./setup_mongodb.sh  # Linux/Mac

# 3. Start Flask
python app.py
```

## Project Structure

```
├── backend/              # Flask Application
│   ├── app.py           # Main Flask app
│   ├── agent.py         # Original LangGraph agent
│   ├── agent_chat.py    # Conversational AI agent
│   ├── templates/       # HTML templates
│   │   ├── base.html
│   │   ├── index.html   # Dashboard
│   │   ├── chat.html    # Chat interface
│   │   ├── login.html
│   │   └── register.html
│   ├── static/          # Static assets
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       ├── app.js   # Dashboard JS
│   │       └── chat.js  # Chat interface JS
│   ├── config/          # Configuration files
│   ├── data/            # Food database
│   └── utils/           # Utilities
├── docs/               # Documentation
│   ├── SETUP.md       # Setup guide
│   ├── ARCHITECTURE.md # System design
│   └── API.md         # API reference
├── Spec.md            # Technical specification
└── Workflow.md        # System workflow
```

## Key Features

### Conversational AI (LangGraph)
- **Fuzzy Matching**: Handles misspellings (e.g., "chiken" → "chicken")
- **Intent Detection**: Understands greetings, questions, and food logging
- **Context Awareness**: Remembers conversation history
- **Natural Responses**: Friendly, encouraging feedback
- **Ingredient Estimation**: Calculates nutrition from ingredients when food is unknown

### ChatGPT-Style Interface
- **Scrollable Chat**: Smooth scrolling message history
- **Message Types**: User messages, AI responses, and AI insights
- **Inline Nutrition**: Food details shown directly in chat
- **Real-time Updates**: Instant feedback and recommendations
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
