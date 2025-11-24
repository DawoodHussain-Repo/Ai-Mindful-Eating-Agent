"""
Gemini AI Nutrition Lookup
Uses Google Gemini to fetch nutrition data for unknown foods
"""

import os
import json
from typing import Dict, Optional, List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

class GeminiNutritionLookup:
    """Use Gemini to get nutrition information for foods"""
    
    def __init__(self):
        """Initialize Gemini API"""
        self.api_key = os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        
        print("✅ Gemini AI initialized for nutrition lookup")
    
    def get_nutrition_data(self, food_name: str, portion_text: str = "1 serving") -> Optional[Dict]:
        """
        Get nutrition data for a food item using Gemini
        
        Args:
            food_name: Name of the food
            portion_text: Portion size description
            
        Returns:
            Dict with nutrition data or None if failed
        """
        
        prompt = f"""You are a nutrition expert. Provide accurate nutrition information for the following food.

Food: {food_name}
Portion: {portion_text}

Return ONLY a valid JSON object with this exact structure (no markdown, no explanation):
{{
    "name": "Food Name",
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
    "fiber": 0,
    "category": "protein|carbs|vegetables|fruits|dairy|fast_food|treats|mixed",
    "confidence": 0.95,
    "source": "gemini"
}}

Rules:
- All numeric values should be for the specified portion
- Use standard serving sizes if portion is unclear
- Category must be one of: protein, carbs, vegetables, fruits, dairy, fast_food, treats, mixed
- Confidence should be 0.8-1.0 based on how common/well-known the food is
- Return realistic, accurate values based on USDA standards
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            # Parse JSON
            nutrition_data = json.loads(response_text)
            
            # Validate required fields
            required_fields = ['calories', 'protein', 'carbs', 'fat', 'fiber', 'category']
            if not all(field in nutrition_data for field in required_fields):
                print(f"⚠️ Gemini response missing required fields for {food_name}")
                return None
            
            # Ensure name is set
            if 'name' not in nutrition_data:
                nutrition_data['name'] = food_name.title()
            
            # Add metadata
            nutrition_data['source'] = 'gemini'
            nutrition_data['confidence'] = nutrition_data.get('confidence', 0.85)
            
            print(f"✅ Gemini found nutrition for: {food_name}")
            return nutrition_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Gemini response for {food_name}: {e}")
            print(f"Response was: {response_text[:200]}")
            return None
        except Exception as e:
            print(f"❌ Gemini API error for {food_name}: {e}")
            return None
    
    def get_nutrition_for_recipe(self, recipe_name: str, ingredients: List[str]) -> Optional[Dict]:
        """
        Get nutrition data for a recipe with multiple ingredients
        
        Args:
            recipe_name: Name of the recipe/dish
            ingredients: List of ingredient names
            
        Returns:
            Dict with combined nutrition data
        """
        
        ingredients_text = ", ".join(ingredients)
        
        prompt = f"""You are a nutrition expert. Analyze this recipe and provide total nutrition information.

Recipe: {recipe_name}
Ingredients: {ingredients_text}

Estimate the nutrition for ONE SERVING of this recipe. Return ONLY a valid JSON object (no markdown):
{{
    "name": "{recipe_name}",
    "calories": 0,
    "protein": 0,
    "carbs": 0,
    "fat": 0,
    "fiber": 0,
    "category": "mixed",
    "confidence": 0.8,
    "source": "gemini",
    "ingredients_used": [list of ingredients]
}}

Consider typical serving sizes and cooking methods. Be realistic and accurate.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown code blocks
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            nutrition_data = json.loads(response_text)
            
            print(f"✅ Gemini analyzed recipe: {recipe_name}")
            return nutrition_data
            
        except Exception as e:
            print(f"❌ Failed to analyze recipe {recipe_name}: {e}")
            return None
    
    def get_meal_suggestions(self, current_nutrition: Dict, daily_goals: Dict) -> List[str]:
        """
        Get meal suggestions based on current nutrition and goals
        
        Args:
            current_nutrition: Current day's nutrition totals
            daily_goals: User's daily nutrition goals
            
        Returns:
            List of meal suggestions
        """
        
        prompt = f"""You are a nutrition coach. Based on the user's current intake and goals, suggest 3 healthy meal options.

Current intake today:
- Calories: {current_nutrition.get('calories', 0)}
- Protein: {current_nutrition.get('protein', 0)}g
- Carbs: {current_nutrition.get('carbs', 0)}g
- Fat: {current_nutrition.get('fat', 0)}g

Daily goals:
- Calories: {daily_goals.get('daily_calories', 2000)}
- Protein: {daily_goals.get('daily_protein', 120)}g
- Carbs: {daily_goals.get('daily_carbs', 250)}g
- Fat: {daily_goals.get('daily_fat', 65)}g

Provide 3 specific meal suggestions that would help them reach their goals. Return ONLY a JSON array:
["Meal suggestion 1", "Meal suggestion 2", "Meal suggestion 3"]

Make suggestions practical, delicious, and nutritionally balanced.
"""
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text.strip()
            
            # Remove markdown
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()
            
            suggestions = json.loads(response_text)
            
            if isinstance(suggestions, list):
                return suggestions[:3]
            
            return []
            
        except Exception as e:
            print(f"❌ Failed to get meal suggestions: {e}")
            return []


# Singleton instance
_gemini_instance = None

def get_gemini_nutrition_lookup() -> GeminiNutritionLookup:
    """Get or create Gemini nutrition lookup instance"""
    global _gemini_instance
    
    if _gemini_instance is None:
        _gemini_instance = GeminiNutritionLookup()
    
    return _gemini_instance
