"""
Food Parser Utility
Handles food text parsing and portion extraction
"""

import re
from typing import Dict, List, Tuple, Any

class FoodParser:
    def __init__(self, food_database: Dict, portion_patterns: Dict, portion_sizes: Dict):
        self.food_database = food_database
        self.portion_patterns = portion_patterns
        self.portion_sizes = portion_sizes
    
    def parse_portion(self, text: str) -> Tuple[float, str]:
        """Extract portion size from text"""
        text = text.lower()
        portion = 1.0
        portion_text = ""
        
        # Check for oz/ounces
        if 'oz' in text or 'ounce' in text:
            match = re.search(self.portion_patterns['oz'], text)
            if match:
                oz_amount = float(match.group(1))
                portion = oz_amount / 4  # 4oz = 1 serving
                portion_text = f"{oz_amount} oz"
                return portion, portion_text
        
        # Check for cups
        if 'cup' in text:
            match = re.search(self.portion_patterns['cup'], text)
            if match:
                cup_str = match.group(1)
                if cup_str in ['1/2', 'half']:
                    portion = 0.5
                    portion_text = "1/2 cup"
                elif cup_str in ['1/4', 'quarter']:
                    portion = 0.25
                    portion_text = "1/4 cup"
                else:
                    portion = float(cup_str)
                    portion_text = f"{portion} cup"
                return portion, portion_text
        
        # Check for grams
        if 'gram' in text or ' g ' in text:
            match = re.search(self.portion_patterns['gram'], text)
            if match:
                grams = float(match.group(1))
                portion = grams / 100  # 100g = 1 serving
                portion_text = f"{grams}g"
                return portion, portion_text
        
        # Check for pieces/slices
        if 'piece' in text or 'slice' in text:
            match = re.search(self.portion_patterns['piece'], text)
            if match:
                pieces = float(match.group(1))
                portion = pieces
                portion_text = f"{int(pieces)} piece{'s' if pieces > 1 else ''}"
                return portion, portion_text
        
        # Check for size descriptors
        for size_word, size_multiplier in self.portion_sizes.items():
            if size_word in text:
                portion = size_multiplier
                portion_text = size_word
                return portion, portion_text
        
        return portion, portion_text or "1 serving"
    
    def parse_food_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse food text and return list of recognized foods"""
        text = text.lower().strip()
        foods_found = []
        
        for food_name, nutrition in self.food_database.items():
            if food_name in text:
                portion, portion_text = self.parse_portion(text)
                
                # Calculate portioned nutrition
                portioned_nutrition = {
                    k: round(v * portion, 1) 
                    for k, v in nutrition.items() 
                    if k != 'category'
                }
                
                foods_found.append({
                    'name': food_name.title(),
                    'portion': portion,
                    'portion_text': portion_text,
                    'nutrition': portioned_nutrition,
                    'category': nutrition['category']
                })
        
        return foods_found
    
    def estimate_from_ingredients(self, ingredients_text: str) -> Dict[str, Any]:
        """Estimate nutrition when exact food not found"""
        estimated = {'calories': 0, 'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0}
        ingredients_found = []
        
        text = ingredients_text.lower()
        
        for food_name, nutrition in self.food_database.items():
            if food_name in text:
                # Use smaller portions for ingredients (0.5 serving default)
                portion = 0.5
                for key in estimated:
                    if key in nutrition:
                        estimated[key] += nutrition[key] * portion
                ingredients_found.append(food_name.title())
        
        if ingredients_found:
            return {
                'success': True,
                'estimated': True,
                'ingredients': ingredients_found,
                'nutrition': {k: round(v, 1) for k, v in estimated.items()}
            }
        
        return {'success': False, 'estimated': False}
