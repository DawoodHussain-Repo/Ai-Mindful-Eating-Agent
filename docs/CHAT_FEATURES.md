# Conversational AI Chat Features

## Overview

The Mindful Eating Agent now includes an advanced conversational AI that understands natural language, handles misspellings, and can calculate nutrition from ingredients.

## Key Features

### 1. Natural Language Understanding

The AI understands casual, conversational input:

```
✅ "had a burger and fries"
✅ "ate two small pizzas"
✅ "just had chicken with rice"
✅ "breakfast was eggs and toast"
```

### 2. Misspelling Tolerance

Uses fuzzy matching to handle typos:

```
User: "chiken and ryce"
AI: Did you mean 'Chicken', 'Rice'? 🤔
```

### 3. Ingredient-Based Calculation

When the AI doesn't recognize a food, it asks for ingredients:

```
User: "pizza"
AI: I don't recognize 'pizza' 🤔

Can you tell me what ingredients are in it?
(e.g., 'bread, cheese, meat, tomato')

User: "bread, cheese, meat, onion"
AI: Got it! Logged: Mixed Dish (1 serving from ingredients) 📝

🧩 Ingredients detected: Bread, Cheese, Meat, Onion

📊 Nutrition:
• 450 calories
• 35g protein
• 45g carbs
• 18g fat
```

### 4. Context Awareness

The AI remembers the conversation:

```
User: "had a burger"
AI: Got it! Logged: Burger (1 serving) 📝

User: "and fries too"
AI: Nice! Added: Fries (1 serving) ✅
```

### 5. Intent Detection

Understands different types of messages:

**Greetings:**
```
User: "hi"
AI: Hey! 👋 What did you eat? Just tell me naturally!
```

**Questions:**
```
User: "how does this work?"
AI: I'm here to help you log your meals! Just tell me what you ate.
```

**Food Logging:**
```
User: "burger"
AI: [Logs the food and shows nutrition]
```

## How It Works

### Food Recognition Pipeline

```
User Input
    ↓
Intent Detection (greeting/question/food)
    ↓
Food Parsing (exact match → fuzzy match → ingredients)
    ↓
Nutrition Calculation
    ↓
Conversational Response
```

### Fuzzy Matching Algorithm

1. **Exact Match**: Checks if food name exists in database
2. **Fuzzy Match**: Uses `difflib.get_close_matches()` with 60% similarity
3. **Ingredient Fallback**: If no match, asks for ingredients

### Ingredient Calculation

When user provides ingredients:

1. Split by commas, "and", semicolons
2. Match each ingredient to database
3. Use 0.5 serving per ingredient (reasonable portion)
4. Sum up all nutrition values
5. Create "Mixed Dish" entry

## Expanded Food Database

Added 200+ common foods including:

**Fast Food:**
- Pizza, Burger, Cheeseburger
- Fries, Hot Dog, Sandwich
- Taco, Burrito

**Snacks:**
- Chips, Popcorn, Pretzels
- Nuts (Almonds, Peanuts, Cashews)
- Crackers

**Treats:**
- Donut, Cookie, Cake
- Ice Cream, Chocolate, Candy

**Dairy:**
- Various cheeses (Cheddar, Mozzarella, Parmesan)
- Milk, Yogurt, Greek Yogurt
- Butter, Cream, Sour Cream

**Vegetables:**
- All common vegetables
- Leafy greens (Spinach, Kale, Lettuce)
- Root vegetables (Potato, Sweet Potato, Carrots)

**Fruits:**
- All common fruits
- Berries (Strawberry, Blueberry, Raspberry)
- Tropical fruits (Mango, Pineapple)

**Carbs:**
- Pasta, Noodles, Spaghetti
- Bread, Toast, Bagel, Croissant
- Oatmeal, Cereal, Granola
- Pancakes, Waffles

## Usage Examples

### Example 1: Simple Food
```
User: "burger"
AI: Got it! Logged: Burger (1 serving) 📝

📊 Nutrition:
• 354 calories
• 20g protein
• 30g carbs
• 17g fat

🔥 That's a solid meal!
```

### Example 2: Multiple Foods
```
User: "two small pizzas"
AI: Nice! I tracked: Pizza (2 servings) ✅

📊 Nutrition:
• 570 calories
• 24g protein
• 72g carbs
• 20g fat
```

### Example 3: Unknown Food with Ingredients
```
User: "shawarma"
AI: I don't recognize 'shawarma' 🤔

Can you tell me what ingredients are in it?

User: "chicken, bread, lettuce, tomato, sauce"
AI: Perfect! Logged: Mixed Dish (1 serving from ingredients) 👍

🧩 Ingredients detected: Chicken, Bread, Lettuce, Tomato

📊 Nutrition:
• 380 calories
• 38g protein
• 42g carbs
• 8g fat

💪 Great protein intake!
```

### Example 4: Misspelling
```
User: "chiken and ryce"
AI: Did you mean 'Chicken', 'Rice'? 🤔

(Reply 'yes' to confirm)

User: "yes"
AI: Awesome! Added: Chicken (1 serving), Rice (1 serving) 🍽️

📊 Nutrition:
• 370 calories
• 35g protein
• 45g carbs
• 4g fat
```

## Technical Implementation

### LangGraph State Machine

```python
ConversationalAgentState:
  - user_message: str
  - intent: str (greeting/question/log_food)
  - parsed_foods: List[Dict]
  - unknown_foods: List[str]
  - needs_clarification: bool
  - agent_response: str
```

### Node Flow

1. **detect_intent_node**: Classify user intent
2. **parse_conversational_food_node**: Extract foods with fuzzy matching
3. **calculate_nutrition_node**: Sum up nutrition values
4. **generate_conversational_response_node**: Create friendly response
5. **generate_recommendations_node**: Add personalized insights

### API Endpoint

**POST** `/api/chat`

Request:
```json
{
  "message": "had a burger",
  "conversation_history": [...]
}
```

Response:
```json
{
  "success": true,
  "agent_response": "Got it! Logged: Burger...",
  "foods": [...],
  "total_nutrition": {...},
  "recommendations": [...],
  "needs_clarification": false
}
```

## Benefits

1. **User-Friendly**: Natural conversation, not forms
2. **Forgiving**: Handles typos and misspellings
3. **Flexible**: Works with known and unknown foods
4. **Educational**: Shows ingredients and nutrition
5. **Fast**: Instant responses, no waiting

## Future Enhancements

- [ ] Voice input support
- [ ] Image recognition for foods
- [ ] Multi-language support
- [ ] Recipe suggestions based on ingredients
- [ ] Nutritional advice in conversation
- [ ] Meal planning through chat

---

**The chat interface makes food logging feel like texting a friend, not filling out a form!** 💬
