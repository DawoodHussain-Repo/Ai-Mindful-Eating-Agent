# API Documentation

## Base URL

```
http://localhost:5000
```

## Authentication

All API endpoints use session-based authentication with HTTP-only cookies.

### Register

**POST** `/register`

Create a new user account with personalized nutrition goals.

**Request Body (form-urlencoded):**
```
email: string (required)
password: string (required)
name: string (required)
goals: JSON string (optional)
```

**Goals Format:**
```json
{
  "daily_calories": 2000,
  "daily_protein": 120,
  "daily_carbs": 250,
  "daily_fat": 65
}
```

**Response:**
- Success: Redirect to dashboard or `200 OK`
- Error: `400 Bad Request` with error message

### Login

**POST** `/login`

Authenticate user and create session.

**Request Body (form-urlencoded):**
```
email: string (required)
password: string (required)
```

**Response:**
- Success: Redirect to dashboard or `200 OK`
- Error: `401 Unauthorized`

### Logout

**GET** `/logout`

End user session.

**Response:**
- Redirect to login page

## Food Logging

### Log Food

**POST** `/api/log-food`

Log a meal with AI-powered food recognition and nutrition analysis.

**Request Body (JSON):**
```json
{
  "food_text": "grilled chicken 6oz, brown rice 1 cup, broccoli",
  "meal_type": "lunch"
}
```

**Meal Types:**
- `breakfast`
- `lunch`
- `dinner`
- `snack`

**Response:**
```json
{
  "success": true,
  "foods": [
    {
      "name": "Grilled Chicken",
      "portion": 1.5,
      "portion_text": "6 oz",
      "nutrition": {
        "calories": 248,
        "protein": 46.5,
        "carbs": 0,
        "fat": 5.4,
        "fiber": 0
      },
      "category": "protein"
    }
  ],
  "total_nutrition": {
    "calories": 485,
    "protein": 52,
    "carbs": 48,
    "fat": 8,
    "fiber": 6
  },
  "recommendations": [],
  "message": "Meal logged successfully with AI analysis!"
}
```

### Get Logs

**GET** `/api/get-logs`

Retrieve today's food logs and daily totals.

**Response:**
```json
{
  "logs": [
    {
      "_id": "507f1f77bcf86cd799439011",
      "timestamp": "2025-11-13T12:30:00",
      "meal_type": "lunch",
      "foods": [...],
      "total_nutrition": {...},
      "original_text": "grilled chicken 6oz..."
    }
  ],
  "daily_total": {
    "calories": 1450,
    "protein": 95,
    "carbs": 180,
    "fat": 45,
    "fiber": 25
  },
  "goals": {
    "daily_calories": 2000,
    "daily_protein": 120,
    "daily_carbs": 250,
    "daily_fat": 65
  }
}
```

## Recommendations

### Get Recommendations

**GET** `/api/get-recommendations`

Get personalized AI recommendations based on eating patterns.

**Response:**
```json
{
  "recommendations": [
    {
      "type": "protein",
      "message": "You're at 45g protein today (goal: 120g). Try adding grilled chicken or Greek yogurt!",
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

**Recommendation Types:**
- `protein` - Protein intake suggestions
- `calories` - Calorie tracking alerts
- `variety` - Food variety suggestions
- `positive` - Positive reinforcement
- `welcome` - Welcome message for new users

## Statistics

### Get Stats

**GET** `/api/get-stats`

Get user eating statistics and patterns.

**Response:**
```json
{
  "stats": {
    "total_meals_logged": 42,
    "avg_daily_calories": 1850,
    "avg_daily_protein": 105,
    "most_common_foods": {
      "Grilled Chicken": 12,
      "Brown Rice": 10,
      "Broccoli": 8
    }
  }
}
```

## Error Responses

All endpoints may return:

**401 Unauthorized**
```json
{
  "error": "Not authenticated"
}
```

**400 Bad Request**
```json
{
  "error": "Please enter food description"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error"
}
```

## CORS

The API supports CORS for the Next.js frontend:

```
Access-Control-Allow-Origin: http://localhost:3000
Access-Control-Allow-Credentials: true
```

## Rate Limiting

Currently no rate limiting is implemented. Consider adding in production.

## Session Management

- Sessions stored in MongoDB
- 7-day session lifetime
- HTTP-only cookies
- Secure flag in production
- SameSite: Lax
