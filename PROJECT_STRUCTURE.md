# Mindful Eating Agent - Project Structure

## Directory Structure

```
AI Mindful Agent/
├── backend/                      # Backend application
│   ├── config/                   # Configuration files (JSON)
│   │   ├── app_config.json      # App settings, patterns, thresholds
│   │   ├── nutrition_goals.json # Default nutrition goals & presets
│   │   └── prompts.json         # User-friendly prompts & messages
│   │
│   ├── data/                     # Data files
│   │   └── food_database.json   # Complete food nutrition database
│   │
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py          # Package initializer
│   │   ├── data_loader.py       # JSON file loader
│   │   ├── food_parser.py       # Food text parsing logic
│   │   ├── recommendation_engine.py  # Recommendation generation
│   │   └── generate_food_db.py  # Script to generate food DB
│   │
│   ├── static/                   # Static assets
│   │   ├── css/
│   │   │   └── style.css        # Application styles
│   │   └── js/
│   │       └── app.js           # Frontend JavaScript
│   │
│   ├── templates/                # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── index.html           # Dashboard
│   │   ├── login.html           # Login page
│   │   └── register.html        # Registration page
│   │
│   ├── app.py                    # Flask application
│   ├── agent.py                  # LangGraph AI agent
│   ├── requirements.txt          # Python dependencies
│   ├── setup.cmd                 # Setup script (Windows)
│   ├── start.cmd                 # Start script (Windows)
│   ├── run.cmd                   # Run script (Windows)
│   └── README.md                 # Backend documentation
│
├── start.cmd                     # Quick start from root
├── QUICKSTART.md                 # Quick start guide
├── PROJECT_STRUCTURE.md          # This file
├── FLOW.md                       # Agent workflow diagram
├── Spec.md                       # Technical specification
└── Workflow.md                   # How the AI works
```

## File Descriptions

### Configuration Files (`backend/config/`)

#### `app_config.json`
Application-wide configuration including:
- App metadata (name, version, host, port)
- Portion parsing patterns (regex)
- Portion size multipliers
- Recommendation thresholds

#### `nutrition_goals.json`
Nutrition goals and presets:
- Default daily goals (calories, protein, carbs, fat, fiber)
- Goal presets (weight loss, muscle gain, maintenance, athletic)

#### `prompts.json`
User-friendly prompts and messages:
- Welcome messages
- Help text
- Error messages
- Encouragement messages

### Data Files (`backend/data/`)

#### `food_database.json`
Comprehensive food nutrition database with 200+ foods:
- Proteins (poultry, seafood, meat, eggs, plant-based)
- Carbs (rice, grains, pasta, bread, potatoes)
- Vegetables (leafy greens, root vegetables)
- Dairy products
- Fruits
- Nuts & seeds
- Fast food & restaurant items
- Snacks & treats
- Condiments & sauces
- Beverages

### Utility Modules (`backend/utils/`)

#### `data_loader.py`
Loads and parses JSON configuration files:
- `load_food_database()` - Load food nutrition data
- `load_user_prompts()` - Load UI prompts
- `load_app_config()` - Load app configuration
- `load_nutrition_goals()` - Load nutrition goals

#### `food_parser.py`
Handles food text parsing:
- `FoodParser` class
- `parse_portion()` - Extract portion sizes
- `parse_food_text()` - Parse food descriptions
- `estimate_from_ingredients()` - Fallback estimation

#### `recommendation_engine.py`
Generates personalized recommendations:
- `RecommendationEngine` class
- `analyze_patterns()` - Analyze eating patterns
- `generate_recommendations()` - Create personalized suggestions

#### `generate_food_db.py`
Script to generate `food_database.json` from Python dict

### Core Application Files

#### `backend/app.py`
Flask web application:
- Route handlers
- API endpoints
- Session management
- Integration with LangGraph agent

#### `backend/agent.py`
LangGraph AI agent:
- Agent state definition
- Node functions (parse, calculate, analyze, recommend)
- Workflow graph
- Agent execution logic

## Data Flow

```
User Input (Text)
    ↓
Flask App (app.py)
    ↓
LangGraph Agent (agent.py)
    ↓
Food Parser (utils/food_parser.py)
    ↓
Food Database (data/food_database.json)
    ↓
Recommendation Engine (utils/recommendation_engine.py)
    ↓
Config & Prompts (config/*.json)
    ↓
Response to User
```

## Configuration Loading

```python
# In agent.py or app.py
from utils.data_loader import (
    load_food_database,
    load_user_prompts,
    load_app_config,
    load_nutrition_goals
)

# Load configurations
food_db = load_food_database()
prompts = load_user_prompts()
config = load_app_config()
goals = load_nutrition_goals()
```

## Adding New Foods

1. Edit `backend/utils/generate_food_db.py`
2. Add food to the appropriate category
3. Run: `python backend/utils/generate_food_db.py`
4. Restart the application

## Modifying Configuration

1. Edit the appropriate JSON file in `backend/config/`
2. Restart the application (changes are loaded on startup)

## Benefits of This Structure

### Separation of Concerns
- Configuration separate from code
- Data separate from logic
- Utilities modular and reusable

### Easy Maintenance
- Update food database without touching code
- Modify prompts without redeployment
- Adjust thresholds via JSON

### Scalability
- Easy to add new food categories
- Simple to extend configuration
- Modular utilities can be reused

### Clarity
- Clear file organization
- Self-documenting structure
- Easy for new developers to understand

## Development Workflow

### 1. Setup
```cmd
start.cmd
```

### 2. Modify Configuration
Edit JSON files in `backend/config/`

### 3. Add Foods
Edit `backend/utils/generate_food_db.py` and run it

### 4. Update Code
Modify `backend/app.py` or `backend/agent.py`

### 5. Test
Access `http://localhost:5000`

### 6. Deploy
Copy entire `backend/` directory to server

## Environment Variables

Set these in production:
- `SECRET_KEY` - Flask secret key
- `DEBUG` - Set to `false` in production
- `DATABASE_URL` - Database connection string (future)

## Future Enhancements

- [ ] Database integration (PostgreSQL)
- [ ] User authentication with JWT
- [ ] API versioning
- [ ] Logging configuration
- [ ] Environment-specific configs
- [ ] Docker containerization
- [ ] CI/CD pipeline configuration
