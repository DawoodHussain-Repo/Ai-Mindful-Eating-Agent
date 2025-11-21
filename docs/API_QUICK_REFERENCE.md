# External API Quick Reference

## Base URL
```
http://localhost:5000/api/v1/agent
```

## Endpoints

### 1. Health Check
```bash
GET /api/v1/agent/health
```

**Response:**
```json
{
  "status": "healthy",
  "service": "Mindful Eating Agent",
  "version": "1.0.0",
  "architecture": "Supervisor-Worker (LangGraph)",
  "database": "connected",
  "capabilities": [
    "food_parsing",
    "nutrition_calculation",
    "pattern_analysis",
    "recommendations"
  ]
}
```

### 2. Process Food Log
```bash
POST /api/v1/agent/process
Content-Type: application/json
```

**Request:**
```json
{
  "user_id": "user123",
  "food_text": "I had grilled chicken and rice for dinner",
  "meal_type": "dinner",
  "user_history": []
}
```

**Response:**
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
    }
  ],
  "total_nutrition": {
    "calories": 370,
    "protein": 35.3,
    "carbs": 45,
    "fat": 4.0,
    "fiber": 0.6
  },
  "recommendations": [
    {
      "icon": "💪",
      "message": "Great protein choice!"
    }
  ],
  "user_message": "Great choice! Grilled Chicken is packed with protein. 💪",
  "needs_clarification": false
}
```

### 3. Get API Schema
```bash
GET /api/v1/agent/schema
```

Returns complete API documentation.

## cURL Examples

### Health Check
```bash
curl http://localhost:5000/api/v1/agent/health
```

### Process Food
```bash
curl -X POST http://localhost:5000/api/v1/agent/process \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user123",
    "food_text": "I had pizza for lunch",
    "meal_type": "lunch"
  }'
```

## Python Example

```python
import requests

# Health check
response = requests.get('http://localhost:5000/api/v1/agent/health')
print(response.json())

# Process food
data = {
    "user_id": "user123",
    "food_text": "I had grilled chicken for dinner",
    "meal_type": "dinner"
}
response = requests.post(
    'http://localhost:5000/api/v1/agent/process',
    json=data
)
result = response.json()
print(f"Calories: {result['total_nutrition']['calories']}")
```

## JavaScript Example

```javascript
// Health check
fetch('http://localhost:5000/api/v1/agent/health')
  .then(res => res.json())
  .then(data => console.log(data));

// Process food
fetch('http://localhost:5000/api/v1/agent/process', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_id: 'user123',
    food_text: 'I had grilled chicken for dinner',
    meal_type: 'dinner'
  })
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "error": "Missing required fields: user_id and food_text"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "error": "Internal server error: ..."
}
```

## Meal Types
Valid values for `meal_type`:
- `breakfast`
- `lunch`
- `dinner`
- `snack`

## Integration Checklist

- [ ] Health check endpoint accessible
- [ ] Process endpoint returns valid JSON
- [ ] Error handling implemented
- [ ] Timeout handling (recommend 5s)
- [ ] Retry logic for failures
- [ ] Logging for debugging
