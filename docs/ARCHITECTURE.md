# System Architecture

## Overview

Mindful Eating Agent is a full-stack AI-powered nutrition tracking application with a Next.js frontend and Flask backend.

## Tech Stack

### Frontend
- **Framework**: Next.js 15 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS v4
- **UI Components**: shadcn/ui
- **State Management**: React Hooks

### Backend
- **Framework**: Flask 3.0
- **Language**: Python 3.10
- **AI/ML**: LangGraph, LangChain
- **Session**: Flask-Session

### Database
- **Primary**: MongoDB 6.0
- **Collections**: users, food_logs, sessions

### Infrastructure
- **Development**: Local (localhost)
- **Production**: AWS (EC2, S3, CloudFront)

## System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   Next.js Frontend                      │
│              (React, TypeScript, Tailwind)              │
│                  Port: 3000                             │
└─────────────────────────────────────────────────────────┘
                          │
                    HTTP/REST API
                    (CORS enabled)
                          │
┌─────────────────────────────────────────────────────────┐
│                   Flask Backend                         │
│              (Python, LangGraph AI)                     │
│                  Port: 5000                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ├─────────────────┐
                          │                 │
┌─────────────────────────▼───┐   ┌────────▼──────────┐
│      MongoDB Database       │   │   LangGraph AI    │
│   (Users, Logs, Sessions)   │   │   Agent Engine    │
│      Port: 27017            │   │                   │
└─────────────────────────────┘   └───────────────────┘
```

## Frontend Architecture

### Pages
```
/                   Landing page
/login              Authentication
/onboarding         3-step user setup
/dashboard          Main application
```

### Components
- **UI Components**: shadcn/ui (Button, Card, Input, etc.)
- **API Client**: Centralized API communication
- **State**: Local React state with hooks

### Data Flow
```
User Action → Component → API Client → Flask Backend
                ↓
         Update UI State
```

## Backend Architecture

### Core Components

**1. Flask Application (app.py)**
- Route handlers
- Session management
- CORS configuration
- Error handling

**2. LangGraph AI Agent (agent.py)**
- Food parsing (NLP)
- Nutrition calculation
- Pattern analysis
- Recommendation generation

**3. MongoDB Client (utils/mongodb_client.py)**
- Database operations
- User management
- Food log storage
- Session persistence

**4. Utilities**
- `data_loader.py` - Load configuration files
- `food_parser.py` - Parse food descriptions
- `recommendation_engine.py` - Generate recommendations

### AI Agent Workflow

```
User Input: "grilled chicken 6oz, brown rice 1 cup"
     ↓
┌────────────────────────────────────────────┐
│  Step 1: Parse Food (NLP)                 │
│  - Extract food items                     │
│  - Parse portions                         │
│  - Match to database                      │
└────────────────────────────────────────────┘
     ↓
┌────────────────────────────────────────────┐
│  Step 2: Calculate Nutrition              │
│  - Lookup nutritional data                │
│  - Calculate totals                       │
│  - Adjust for portions                    │
└────────────────────────────────────────────┘
     ↓
┌────────────────────────────────────────────┐
│  Step 3: Analyze Patterns                 │
│  - Review user history                    │
│  - Detect eating patterns                 │
│  - Identify trends                        │
└────────────────────────────────────────────┘
     ↓
┌────────────────────────────────────────────┐
│  Step 4: Generate Recommendations         │
│  - Compare to goals                       │
│  - Create personalized suggestions        │
│  - Provide positive reinforcement         │
└────────────────────────────────────────────┘
     ↓
Return: Foods, Nutrition, Recommendations
```

## Database Schema

### users
```javascript
{
  _id: ObjectId,
  email: String (unique),
  name: String,
  password: String (hashed),
  created_at: DateTime,
  goals: {
    daily_calories: Number,
    daily_protein: Number,
    daily_carbs: Number,
    daily_fat: Number
  }
}
```

### food_logs
```javascript
{
  _id: ObjectId,
  user_id: String,
  timestamp: DateTime,
  meal_type: String,
  foods: [{
    name: String,
    portion: Number,
    portion_text: String,
    nutrition: Object,
    category: String
  }],
  total_nutrition: {
    calories: Number,
    protein: Number,
    carbs: Number,
    fat: Number,
    fiber: Number
  },
  original_text: String
}
```

### sessions
```javascript
{
  _id: ObjectId,
  session_id: String (unique),
  user_id: String,
  created_at: DateTime,
  expiry: DateTime
}
```

## Security

### Authentication
- Password hashing: bcrypt
- Session-based auth
- HTTP-only cookies
- 7-day session lifetime

### Data Protection
- CORS: Restricted to frontend origin
- Input validation
- SQL injection: N/A (NoSQL)
- XSS protection: React escaping

### MongoDB Security
- Local development: No auth
- Production: Authentication required
- Network: Localhost only (dev)

## Performance

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- Caching strategies

### Backend
- Database indexing
- Query optimization
- Connection pooling
- Response caching

### Database Indexes
```javascript
users.email (unique)
food_logs.user_id
food_logs.timestamp
food_logs.user_id + timestamp (compound)
sessions.session_id (unique)
sessions.expiry
```

## Scalability

### Horizontal Scaling
- Stateless API design
- Session storage in MongoDB
- Load balancer ready

### Vertical Scaling
- Database optimization
- Query performance
- Connection management

## Monitoring

### Logs
- Flask application logs
- MongoDB query logs
- Error tracking

### Metrics
- API response times
- Database query performance
- User activity patterns

## Deployment

### Development
```
Frontend: npm run dev (port 3000)
Backend: python app.py (port 5000)
Database: MongoDB local (port 27017)
```

### Production
```
Frontend: Vercel or AWS S3 + CloudFront
Backend: AWS EC2 with Gunicorn
Database: MongoDB Atlas or AWS DocumentDB
```

## Configuration Files

```
backend/config/
├── mongodb_config.json      # Database settings
├── app_config.json          # Application settings
├── nutrition_goals.json     # Default nutrition goals
└── prompts.json             # AI prompts

backend/data/
└── food_database.json       # Nutritional database

frontend/
└── .env.local               # Environment variables
```

## Development Workflow

1. Start MongoDB
2. Start Flask backend
3. Start Next.js frontend
4. Make changes
5. Test locally
6. Commit to Git
7. Deploy to production

## Future Enhancements

- Real-time notifications
- Mobile app (React Native)
- Advanced analytics
- Social features
- Recipe recommendations
- Barcode scanning
- Voice input
