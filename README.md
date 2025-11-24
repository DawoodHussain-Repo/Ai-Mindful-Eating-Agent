# AI Mindful Eating Agent

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-0.4.x-orange.svg)](https://www.trychroma.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

> An intelligent conversational AI agent for nutrition tracking and mindful eating guidance using LangGraph and Google Gemini AI.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [Team](#team)

## 🎯 Overview

The AI Mindful Eating Agent is a sophisticated web-based application that simplifies nutrition tracking through natural language processing. Users can log meals conversationally (e.g., "I had grilled chicken and rice"), and the system automatically calculates nutritional information, tracks eating patterns, and provides personalized recommendations.

### Problem Statement

Traditional calorie counting apps are:
- **Tedious**: Manual database searches for every food item
- **Generic**: One-size-fits-all advice that doesn't adapt to individual needs
- **Complex**: Requires nutritional knowledge to use effectively

### Our Solution

An AI-powered agent that:
- ✅ Understands natural language food descriptions
- ✅ Automatically calculates nutrition (calories, protein, carbs, fat, fiber)
- ✅ Learns from eating patterns to provide personalized insights
- ✅ Integrates with Google Gemini AI for unknown food recognition
- ✅ Uses a 3-tier smart caching system for optimal performance

## ✨ Features

### Core Functionality
- **Natural Language Processing**: Parse food descriptions like "2 eggs and toast"
- **Automatic Nutrition Calculation**: Instant macronutrient breakdown
- **Conversational Interface**: Chat-based food logging
- **Pattern Analysis**: Identify eating habits and trends
- **Personalized Recommendations**: AI-driven dietary suggestions
- **Progress Tracking**: Calendar view of nutrition history

### Technical Features
- **Supervisor-Worker Architecture**: LangGraph-based agent orchestration
- **3-Tier Smart Caching**:
  1. Static food database (156 common foods)
  2. ChromaDB cache for learned foods
  3. Google Gemini AI for unknown foods
- **Lazy Loading**: On-demand food database loading for fast startup
- **Session Management**: Secure user authentication and session handling
- **RESTful API**: External integration support
- **Health Monitoring**: System status endpoints

## 🏗️ Architecture

The system uses a **Supervisor-Worker** pattern orchestrated by LangGraph:

```
┌─────────────┐
│   User      │
│   Input     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│   Supervisor    │◄──────┐
│   (LangGraph)   │       │
└────────┬────────┘       │
         │                │
    ┌────┴────┬───────────┼──────────┬─────────┐
    ▼         ▼           ▼          ▼         ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│ Food   │ │Nutrition│ │Pattern │ │Recom-  │ │Response│
│ Parser │ │  Calc   │ │Analyst │ │mender  │ │  Gen   │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │         │           │          │         │
    └─────────┴───────────┴──────────┴─────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │  ChromaDB   │
                  │  (Storage)  │
                  └─────────────┘
```

**See [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design documentation.**

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask 3.0.0 (Python web framework)
- **AI/ML**: 
  - LangGraph (Agent workflow orchestration)
  - LangChain (LLM integration)
  - Google Gemini AI (Intelligent food recognition)
  - Sentence Transformers (Embeddings)
- **Database**: ChromaDB 0.4.x (Vector database for caching)
- **Session**: Flask-Session (User session management)

### Frontend
- **Templates**: Jinja2 (Flask templating)
- **Styling**: Custom CSS
- **JavaScript**: Vanilla JS for interactivity

### DevOps
- **Version Control**: Git
- **Environment**: Python 3.9-3.12 (ChromaDB compatibility)
- **Package Management**: pip + requirements.txt

## 📦 Installation

### Prerequisites
- Python 3.9, 3.10, 3.11, or 3.12 (ChromaDB not compatible with 3.13+)
- Git
- Google Gemini API Key ([Get one here](https://makersuite.google.com/app/apikey))

### Quick Start

1. **Clone the repository**
```bash
git clone https://github.com/your-org/ai-mindful-eating-agent.git
cd ai-mindful-eating-agent
```

2. **Set up environment variables**
```bash
cd backend
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. **Run the application**
```bash
# On Windows
..\start-fullstack.cmd

# On Linux/Mac
chmod +x start-fullstack.sh
./start-fullstack.sh
```

The script will:
- Create a Python 3.9 virtual environment
- Install all dependencies
- Start the Flask server on http://localhost:5000

### Manual Installation

```bash
# Create virtual environment
python3.9 -m venv backend/venv39

# Activate virtual environment
# Windows:
backend\venv39\Scripts\activate
# Linux/Mac:
source backend/venv39/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Run the application
python app.py
```

## 🚀 Usage

### Web Interface

1. **Register/Login**: Create an account at http://localhost:5000/login
2. **Log Food**: Use the chat interface to log meals
   - "I had grilled chicken and brown rice"
   - "2 eggs and toast for breakfast"
   - "Pizza slice and salad"
3. **View Progress**: Check the calendar view for nutrition history
4. **Get Recommendations**: Receive personalized dietary suggestions

### API Usage

```python
import requests

# Log food via API
response = requests.post('http://localhost:5000/api/log-food', json={
    'food_text': 'grilled chicken and rice',
    'meal_type': 'lunch'
}, cookies={'session': 'your_session_cookie'})

print(response.json())
# {
#   "success": true,
#   "foods": [...],
#   "total_nutrition": {"calories": 450, "protein": 35, ...},
#   "recommendations": [...]
# }
```

**See [API.md](docs/API.md) for complete API documentation.**

## 📁 Project Structure

```
ai-mindful-eating-agent/
├── backend/
│   ├── api/                    # External API endpoints
│   ├── config/                 # Configuration files
│   ├── data/                   # Static food database
│   ├── static/                 # CSS, JS, images
│   ├── templates/              # HTML templates
│   ├── utils/                  # Utility modules
│   │   ├── chromadb_client.py  # Database operations
│   │   ├── gemini_nutrition.py # Gemini AI integration
│   │   ├── nutrition_cache.py  # Smart caching system
│   │   └── chroma_session.py   # Session management
│   ├── agent.py                # LangGraph agent logic
│   ├── agent_chat.py           # Conversational agent
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   └── .env                    # Environment variables
├── docs/                       # Documentation
│   ├── ARCHITECTURE.md         # System architecture
│   ├── API.md                  # API documentation
│   ├── final_report.pdf        # Project report
│   └── Assignment04/           # Project management artifacts
├── tests/                      # Test files
│   ├── test_chromadb.py
│   ├── test_integration.py
│   └── test_simple.py
├── start-fullstack.cmd         # Windows startup script
├── README.md                   # This file
└── .gitignore
```

## 🧪 Testing

Run the test suite:

```bash
# Activate virtual environment
cd backend
.\venv39\Scripts\activate  # Windows
# source venv39/bin/activate  # Linux/Mac

# Run all tests
cd ../tests
python -m pytest

# Run specific test
python test_integration.py
```

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: End-to-end workflow testing
- **API Tests**: RESTful endpoint validation

## 📊 Project Management

This project was developed using rigorous software project management practices:

- **Work Breakdown Structure (WBS)**: 5 phases, 25+ work packages
- **Schedule Management**: 119-day timeline with resource leveling
- **Cost Estimation**: $150,000 budget with EVM tracking
- **Risk Management**: Identified and mitigated 6 key risks
- **Quality Assurance**: 90%+ food recognition accuracy target

**See [docs/final_report.pdf](docs/final_report.pdf) for complete project documentation.**

### Key Metrics
- **Schedule Performance Index (SPI)**: 1.058 (5.8% ahead of schedule)
- **Cost Performance Index (CPI)**: 1.019 (under budget)
- **Food Recognition Accuracy**: 90%+
- **API Response Time**: <500ms
- **System Uptime**: 99%+

## 👥 Team

**FAST National University - Islamabad Campus**  
**Course**: Fundamentals of Software Project Management  
**Section**: E

| Name | Roll Number | Role |
|------|-------------|------|
| Dawood Hussain | 22i-2410 | Project Manager |
| Gulsher Khan | 22i-2637 | Technical Lead |
| Ahsan Faraz | 22i-8791 | AI/ML Developer |

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Google Gemini AI** for intelligent food recognition
- **LangChain/LangGraph** for agent orchestration framework
- **ChromaDB** for vector database capabilities
- **Flask** community for excellent web framework
- **FAST University** for project guidance and support

## 📞 Contact

For questions or support, please contact:
- **Email**: [project-email@example.com](mailto:project-email@example.com)
- **GitHub Issues**: [Create an issue](https://github.com/your-org/ai-mindful-eating-agent/issues)

---

**Built with ❤️ by Team Mindful Eating**
