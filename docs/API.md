# API Documentation

## AI Mindful Eating Agent - RESTful API Reference

**Base URL**: `http://localhost:5000`  
**Version**: 1.0  
**Last Updated**: November 25, 2025

---

## Table of Contents

1. [Authentication](#authentication)
2. [Endpoints](#endpoints)
   - [Health Check](#health-check)
   - [User Management](#user-management)
   - [Food Logging](#food-logging)
   - [Nutrition Data](#nutrition-data)
   - [Recommendations](#recommendations)
   - [Chat Interface](#chat-interface)
3. [Error Handling](#error-handling)
4. [Rate Limiting](#rate-limiting)
5. [Examples](#examples)

---

## Authentication

The API uses **session-based authentication** with HTTP-only cookies.

### Login Flow

1. **Register** or **Login** to obtain a session cookie
2. Include the session cookie in subsequent requests
3. Session expires after 7 days of inactivity

**Session Cookie Name**: `mindful_eating_session`

---

## Endpoints

### Health Check

#### GET /health

Check if the service is running and database is connected.

**Authentication**: Not required

**Response**:
```json
{
  "status": "healthy",
  "service": "Mindful Eating Agent API",
  "timestamp": "2025-11-25T12:00:00.000Z",
  "database": "ChromaDB",
  "database_status": "connected",
  "version": "1.0.0"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service is down

---

### User Management

#### POST /register

Create a new user account.

**Authentication**: Not required

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe",
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

**Response** (Success):
```json
{
  "success": true
}
```

**Response** (Error):
```json
{
  "error": "Email already registered"
}
```

**Status Codes**:
- `200 OK`: Registration successful
- `400 Bad Request`: Invalid input or email already exists

---

#### POST /login

Authenticate a user and create a session.

**Authentication**: Not required

**Request Body** (Form Data):
```
email=user@example.com
password=securePassword123
```

**Response**: Redirects to `/` with session cookie set

**Status Codes**:
- `302 Found`: Login successful, redirect to dashboard
- `200 OK`: Login page with error message

---

#### GET /logout

End the current user session.

**Authentication**: Required

**Response**: Redirects to `/login`

**Status Codes**:
- `302 Found`: Logout successful

---

### Food Logging

#### POST /api/log-food

Log a meal with natural language input.

**Authentication**: Required

**Request Body**:
```json
{
  "food_text": "grilled chicken breast and brown rice",
  "meal_type": "lunch"
}
```

**Parameters**:
- `food_text` (string, required): Natural language description of food
- `meal_type` (string, required): One of `breakfast`, `lunch`, `dinner`, `snack`

**Response** (Success):
```json
{
  "success": true,
  "foods": [
    {
      "name": "Grilled Chicken",
      "portion": 1.0,
      "portion_text": "1 serving",
      "nutrition": {
        "calories": 165,
        "protein": 31,
        "carbs": 0,
        "fat": 3.6,
        "fiber": 0
      },
      "category": "protein"
    },
    {
      "name": "Brown Rice",
      "portion": 1.0,
      "portion_text": "1 serving",
      "nutrition": {
        "calories": 216,
        "protein": 5,
        "carbs": 45,
        "fat": 1.8,
        "fiber": 3.5
      },
      "category": "carbs"
    }
  ],
  "total_nutrition": {
    "calories": 381,
    "protein": 36,
    "carbs": 45,
    "fat": 5.4,
    "fiber": 3.5
  },
  "recommendations": [
    {
      "type": "positive",
      "message": "Excellent protein intake! You're on track for your goals.",
      "icon": "✅"
    }
  ],
  "message": "Meal logged successfully with AI analysis!"
}
```

**Response** (Error):
```json
{
  "error": "No food items recognized. Try being more specific."
}
```

**Status Codes**:
- `200 OK`: Food logged successfully
- `400 Bad Request`: Invalid input or no food recognized
- `401 Unauthorized`: Not authenticated

---

### Nutrition Data

#### GET /api/get-logs

Get today's food logs and daily totals.

**Authentication**: Required

**Response**:
```json
{
  "logs": [
    {
      "_id": "log_uuid_1",
      "user_id": "user_uuid",
      "timestamp": "2025-11-25T08:30:00Z",
      "meal_type": "breakfast",
      "foods": [...],
      "total_nutrition": {
        "calories": 350,
        "protein": 20,
        "carbs": 45,
        "fat": 10,
        "fiber": 5
      },
      "original_text": "2 eggs and toast"
    },
    {
      "_id": "log_uuid_2",
      "user_id": "user_uuid",
      "timestamp": "2025-11-25T12:30:00Z",
      "meal_type": "lunch",
      "foods": [...],
      "total_nutrition": {
        "calories": 450,
        "protein": 35,
        "carbs": 50,
        "fat": 12,
        "fiber": 6
      },
      "original_text": "grilled chicken and rice"
    }
  ],
  "daily_total": {
    "calories": 800,
    "protein": 55,
    "carbs": 95,
    "fat": 22,
    "fiber": 11
  },
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

**Status Codes**:
- `200 OK`: Logs retrieved successfully
- `401 Unauthorized`: Not authenticated

---

#### GET /api/get-stats

Get eating pattern statistics (last 14 days).

**Authentication**: Required

**Response**:
```json
{
  "stats": {
    "total_meals_logged": 42,
    "avg_daily_calories": 1850,
    "avg_daily_protein": 95,
    "most_common_foods": {
      "Grilled Chicken": 8,
      "Brown Rice": 7,
      "Eggs": 6,
      "Broccoli": 5,
      "Banana": 4
    }
  }
}
```

**Status Codes**:
- `200 OK`: Stats retrieved successfully
- `401 Unauthorized`: Not authenticated

---

#### GET /api/calendar-logs

Get logs organized by date for calendar view.

**Authentication**: Required

**Query Parameters**:
- `days` (integer, optional): Number of days to retrieve (default: 30)

**Example**: `/api/calendar-logs?days=30`

**Response**:
```json
{
  "calendar": [
    {
      "date": "2025-11-25",
      "data": {
        "meals": [...],
        "total_calories": 1850,
        "total_protein": 95,
        "total_carbs": 220,
        "total_fat": 60,
        "meal_count": 3
      }
    },
    {
      "date": "2025-11-24",
      "data": {
        "meals": [...],
        "total_calories": 1920,
        "total_protein": 100,
        "total_carbs": 230,
        "total_fat": 65,
        "meal_count": 4
      }
    }
  ]
}
```

**Status Codes**:
- `200 OK`: Calendar data retrieved successfully
- `401 Unauthorized`: Not authenticated

---

### Recommendations

#### GET /api/get-recommendations

Get personalized dietary recommendations based on current progress.

**Authentication**: Required

**Response**:
```json
{
  "recommendations": [
    {
      "type": "protein",
      "message": "You're at 55g protein today (goal: 120g). Try adding grilled chicken, salmon, or Greek yogurt!",
      "icon": "💪"
    },
    {
      "type": "positive",
      "message": "Great job staying within your calorie budget today!",
      "icon": "✅"
    }
  ]
}
```

**Recommendation Types**:
- `protein`: Protein intake suggestions
- `calories`: Calorie management tips
- `variety`: Food variety recommendations
- `positive`: Positive reinforcement
- `welcome`: Welcome message for new users

**Status Codes**:
- `200 OK`: Recommendations retrieved successfully
- `401 Unauthorized`: Not authenticated

---

#### GET /api/weekly-insight

Get weekly eating pattern analysis and suggestions.

**Authentication**: Required

**Query Parameters**:
- `days` (integer, optional): Number of days to analyze (default: 7)

**Example**: `/api/weekly-insight?days=7`

**Response**:
```json
{
  "summary": {
    "days_considered": 7,
    "avg_calories": 1875,
    "avg_protein": 98,
    "avg_carbs": 225,
    "fast_food_meals": 2,
    "vegetable_meals": 5,
    "fruit_meals": 4
  },
  "insight": "In the last 7 days, you averaged about 1875 calories, 98g protein, and 225g carbs per day.",
  "suggestions": [
    "You've had fast food or treats several times. Try swapping one of those meals for a lighter home-cooked option this week.",
    "Most days could use more veggies. Aim to add at least one colorful vegetable to your main meals."
  ]
}
```

**Status Codes**:
- `200 OK`: Insights retrieved successfully
- `401 Unauthorized`: Not authenticated

---

### Chat Interface

#### POST /api/chat

Conversational food logging with natural language understanding.

**Authentication**: Required

**Request Body**:
```json
{
  "message": "I had chicken and rice for lunch",
  "conversation_history": [
    {
      "role": "user",
      "content": "What should I eat for lunch?"
    },
    {
      "role": "assistant",
      "content": "How about grilled chicken with brown rice and vegetables?"
    }
  ]
}
```

**Parameters**:
- `message` (string, required): User's message
- `conversation_history` (array, optional): Previous conversation context

**Response** (Food Logging):
```json
{
  "success": true,
  "intent": "log_food",
  "agent_response": "Great choice! I've logged your lunch. You had 450 calories with 35g of protein. You're doing well on your protein goal today!",
  "foods": [...],
  "total_nutrition": {...},
  "recommendations": [...]
}
```

**Response** (Information Request):
```json
{
  "success": true,
  "intent": "info_request",
  "agent_response": "Grilled chicken is an excellent source of lean protein with about 165 calories and 31g of protein per serving. It's low in fat and carbs, making it perfect for muscle building and weight management.",
  "needs_clarification": false
}
```

**Response** (Clarification Needed):
```json
{
  "success": false,
  "intent": "clarification",
  "agent_response": "I noticed you mentioned chicken. What type did you have? Grilled, fried, or baked?",
  "needs_clarification": true
}
```

**Status Codes**:
- `200 OK`: Message processed successfully
- `400 Bad Request`: Empty message
- `401 Unauthorized`: Not authenticated

---

#### GET /api/chat-daily-suggestion

Get AI-generated daily nutrition summary and suggestions.

**Authentication**: Required

**Response**:
```json
{
  "success": true,
  "agent_response": "So far today you're at 800 calories and 55g protein. Great lunch! You're hitting your protein goals and staying within your calorie budget. Keep it up! 🎉",
  "recommendations": [...],
  "daily_total": {
    "calories": 800,
    "protein": 55,
    "carbs": 95,
    "fat": 22,
    "fiber": 11
  },
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

**Status Codes**:
- `200 OK`: Suggestion generated successfully
- `401 Unauthorized`: Not authenticated

---

#### GET /api/meal-suggestions

Get AI-powered meal suggestions based on current nutrition.

**Authentication**: Required

**Response**:
```json
{
  "success": true,
  "suggestions": [
    {
      "meal": "Grilled Salmon with Quinoa",
      "reason": "You need more protein and omega-3s",
      "nutrition": {
        "calories": 450,
        "protein": 40,
        "carbs": 45,
        "fat": 15
      }
    },
    {
      "meal": "Greek Yogurt with Berries",
      "reason": "Light snack to boost protein",
      "nutrition": {
        "calories": 150,
        "protein": 17,
        "carbs": 15,
        "fat": 2
      }
    }
  ],
  "current_nutrition": {
    "calories": 800,
    "protein": 55,
    "carbs": 95,
    "fat": 22
  },
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

**Status Codes**:
- `200 OK`: Suggestions generated successfully
- `401 Unauthorized`: Not authenticated
- `500 Internal Server Error`: AI service unavailable

---

## Error Handling

### Error Response Format

All error responses follow this structure:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Meaning | Common Causes |
|-------------|---------|---------------|
| 400 | Bad Request | Invalid input, missing required fields |
| 401 | Unauthorized | Not logged in, session expired |
| 404 | Not Found | Endpoint doesn't exist |
| 500 | Internal Server Error | Database error, AI service down |
| 503 | Service Unavailable | System maintenance, database offline |

### Error Examples

**401 Unauthorized**:
```json
{
  "error": "Not authenticated"
}
```

**400 Bad Request**:
```json
{
  "error": "Please enter food description"
}
```

**500 Internal Server Error**:
```json
{
  "error": "Failed to process request. Please try again."
}
```

---

## Rate Limiting

**Current Status**: Not implemented (planned for production)

**Planned Limits**:
- 100 requests per minute per user
- 1000 requests per hour per user
- 429 Too Many Requests response when exceeded

---

## Examples

### Example 1: Complete Food Logging Flow

```python
import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# 1. Register
response = session.post(f"{BASE_URL}/register", json={
    "email": "john@example.com",
    "password": "securePass123",
    "name": "John Doe"
})
print(response.json())  # {"success": true}

# 2. Log breakfast
response = session.post(f"{BASE_URL}/api/log-food", json={
    "food_text": "2 eggs and toast",
    "meal_type": "breakfast"
})
print(response.json())
# {
#   "success": true,
#   "foods": [...],
#   "total_nutrition": {"calories": 350, "protein": 20, ...}
# }

# 3. Get today's logs
response = session.get(f"{BASE_URL}/api/get-logs")
print(response.json())
# {
#   "logs": [...],
#   "daily_total": {"calories": 350, "protein": 20, ...}
# }

# 4. Get recommendations
response = session.get(f"{BASE_URL}/api/get-recommendations")
print(response.json())
# {
#   "recommendations": [...]
# }
```

### Example 2: Conversational Chat

```python
import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login first (assuming already registered)
session.post(f"{BASE_URL}/login", data={
    "email": "john@example.com",
    "password": "securePass123"
})

# Chat conversation
conversation = []

# User asks a question
response = session.post(f"{BASE_URL}/api/chat", json={
    "message": "What's a good high-protein lunch?",
    "conversation_history": conversation
})
result = response.json()
print(result["agent_response"])
# "A great high-protein lunch would be grilled chicken with quinoa..."

conversation.append({"role": "user", "content": "What's a good high-protein lunch?"})
conversation.append({"role": "assistant", "content": result["agent_response"]})

# User logs food
response = session.post(f"{BASE_URL}/api/chat", json={
    "message": "I had grilled chicken and quinoa",
    "conversation_history": conversation
})
result = response.json()
print(result["agent_response"])
# "Excellent choice! I've logged your lunch. You had 450 calories..."
print(result["total_nutrition"])
# {"calories": 450, "protein": 45, ...}
```

### Example 3: Weekly Analysis

```python
import requests

BASE_URL = "http://localhost:5000"
session = requests.Session()

# Login
session.post(f"{BASE_URL}/login", data={
    "email": "john@example.com",
    "password": "securePass123"
})

# Get weekly insight
response = session.get(f"{BASE_URL}/api/weekly-insight?days=7")
insight = response.json()

print(f"Average daily calories: {insight['summary']['avg_calories']}")
print(f"Average daily protein: {insight['summary']['avg_protein']}g")
print(f"\nInsight: {insight['insight']}")
print("\nSuggestions:")
for suggestion in insight['suggestions']:
    print(f"  - {suggestion}")
```

---

## Integration with Supervisor System

### External API Endpoint

For supervisor system integration, use the dedicated endpoint:

**POST /api/v1/agent/process**

```json
{
  "user_id": "external_user_123",
  "food_text": "grilled chicken and rice",
  "meal_type": "lunch"
}
```

**Response**:
```json
{
  "success": true,
  "foods": [...],
  "total_nutrition": {...},
  "message": "Meal logged successfully"
}
```

This endpoint is designed for external systems to integrate with the Mindful Eating Agent as a worker in a supervisor-worker architecture.

---

## Changelog

### Version 1.0 (November 25, 2025)
- Initial API release
- All core endpoints implemented
- Session-based authentication
- ChromaDB integration
- Google Gemini AI integration

---

## Support

For API support or questions:
- **Email**: support@mindful-eating-agent.com
- **GitHub Issues**: [Create an issue](https://github.com/your-org/ai-mindful-eating-agent/issues)
- **Documentation**: [Full Documentation](../README.md)

---

**API Version**: 1.0  
**Last Updated**: November 25, 2025  
**Maintained by**: Team Mindful Eating
