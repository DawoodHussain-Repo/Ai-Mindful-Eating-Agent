import json

# Load existing database
with open('backend/data/food_database.json', 'r', encoding='utf-8') as f:
    food_db = json.load(f)

# Add beverages
beverages = {
    "pepsi": {"calories": 150, "protein": 0, "carbs": 41, "fat": 0, "fiber": 0, "category": "beverages"},
    "coke": {"calories": 140, "protein": 0, "carbs": 39, "fat": 0, "fiber": 0, "category": "beverages"},
    "coca cola": {"calories": 140, "protein": 0, "carbs": 39, "fat": 0, "fiber": 0, "category": "beverages"},
    "sprite": {"calories": 140, "protein": 0, "carbs": 38, "fat": 0, "fiber": 0, "category": "beverages"},
    "fanta": {"calories": 160, "protein": 0, "carbs": 44, "fat": 0, "fiber": 0, "category": "beverages"},
    "mountain dew": {"calories": 170, "protein": 0, "carbs": 46, "fat": 0, "fiber": 0, "category": "beverages"},
    "soda": {"calories": 150, "protein": 0, "carbs": 40, "fat": 0, "fiber": 0, "category": "beverages"},
    "orange juice": {"calories": 112, "protein": 1.7, "carbs": 26, "fat": 0.5, "fiber": 0.5, "category": "beverages"},
    "apple juice": {"calories": 114, "protein": 0.1, "carbs": 28, "fat": 0.3, "fiber": 0.2, "category": "beverages"},
    "juice": {"calories": 110, "protein": 1, "carbs": 26, "fat": 0.3, "fiber": 0.3, "category": "beverages"},
    "coffee": {"calories": 2, "protein": 0.3, "carbs": 0, "fat": 0, "fiber": 0, "category": "beverages"},
    "tea": {"calories": 2, "protein": 0, "carbs": 0.7, "fat": 0, "fiber": 0, "category": "beverages"},
    "water": {"calories": 0, "protein": 0, "carbs": 0, "fat": 0, "fiber": 0, "category": "beverages"},
    "smoothie": {"calories": 145, "protein": 3, "carbs": 32, "fat": 1.5, "fiber": 3, "category": "beverages"},
    "protein shake": {"calories": 160, "protein": 25, "carbs": 10, "fat": 3, "fiber": 1, "category": "beverages"}
}

# Merge
food_db.update(beverages)

# Save
with open('backend/data/food_database.json', 'w', encoding='utf-8') as f:
    json.dump(food_db, f, indent=2)

print(f"✅ Added {len(beverages)} beverages to database. Total foods: {len(food_db)}")
