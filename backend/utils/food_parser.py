"""
Enhanced Food Parser with Gemini AI integration
Handles natural language, asks clarifying questions, and uses AI for unknown foods
"""

import re
from typing import Dict, List, Tuple, Any, Optional

class FoodParser:
    def __init__(self, food_database: Dict, portion_patterns: Dict, portion_sizes: Dict, 
                 nutrition_cache=None, gemini_lookup=None):
        self.food_database = food_database
        self.portion_patterns = portion_patterns
        self.portion_sizes = portion_sizes
        self.nutrition_cache = nutrition_cache
        self.gemini_lookup = gemini_lookup
        
        # Build synonym mappings for better recognition
        self.synonyms = {
            'had': 'ate', 'consumed': 'ate', 'eating': 'ate', 'having': 'ate',
            'drank': 'drink', 'drinking': 'drink',
            'dinner': 'meal', 'lunch': 'meal', 'breakfast': 'meal', 'snack': 'meal'
        }
        
        # Generic terms that need clarification
        self.generic_terms = {
            'soda': ['pepsi', 'coke', 'sprite', 'fanta', 'mountain dew'],
            'juice': ['orange juice', 'apple juice'],
            'meat': ['chicken', 'beef', 'pork', 'turkey'],
            'fish': ['salmon', 'tuna', 'cod', 'tilapia']
        }
    
    def normalize_text(self, text: str) -> str:
        """Normalize text by removing filler words and applying synonyms"""
        text = text.lower().strip()
        
        # Remove common filler words
        fillers = ['i', 'a', 'an', 'the', 'some', 'for', 'my', 'today', 'just', 'ate', 'had', 'drank']
        words = text.split()
        words = [w for w in words if w not in fillers or len(words) <= 3]
        
        return ' '.join(words)
    
    def check_for_generic_terms(self, text: str) -> Optional[Dict[str, Any]]:
        """Check if user mentioned a generic term that needs clarification"""
        text_lower = text.lower()
        
        for generic, options in self.generic_terms.items():
            # Check if generic term is mentioned but no specific option
            if generic in text_lower:
                # Check if any specific option is already mentioned
                has_specific = any(opt in text_lower for opt in options)
                if not has_specific:
                    return {
                        'needs_clarification': True,
                        'generic_term': generic,
                        'options': options,
                        'question': f"Which {generic}? ({', '.join(options[:3])}...)"
                    }
        return None
    
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
    
    def fuzzy_match_food(self, text: str) -> List[str]:
        """Find foods using fuzzy matching - handles variations and word order"""
        text_normalized = self.normalize_text(text)
        text_words = set(text_normalized.split())
        
        matched_foods = []
        
        for food_name in self.food_database.keys():
            food_words = set(food_name.split())
            
            # Direct substring match
            if food_name in text.lower():
                matched_foods.append(food_name)
                continue
            
            # Word overlap match (at least 50% of food name words present)
            if food_words and len(food_words & text_words) >= len(food_words) * 0.5:
                matched_foods.append(food_name)
        
        return matched_foods
    
    def parse_food_text(self, text: str) -> List[Dict[str, Any]]:
        """Parse food text and return list of recognized foods"""
        text = text.lower().strip()
        
        # First check for generic terms that need clarification
        clarification_check = self.check_for_generic_terms(text)
        if clarification_check:
            return [{
                'needs_clarification': True,
                'question': clarification_check['question']
            }]
        
        foods_found = []
        
        # Try fuzzy matching in static database first
        matched_food_names = self.fuzzy_match_food(text)
        
        for food_name in matched_food_names:
            nutrition = self.food_database[food_name]
            portion, portion_text = self.parse_portion(text)
            
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
                'category': nutrition['category'],
                'source': 'static'
            })
        
        # If no matches in static DB, try cache
        if not foods_found and self.nutrition_cache:
            cached_nutrition = self.nutrition_cache.get(text)
            if cached_nutrition:
                portion, portion_text = self.parse_portion(text)
                
                portioned_nutrition = {
                    k: round(v * portion, 1) 
                    for k, v in cached_nutrition.items() 
                    if k not in ['category', 'source', 'cached_at', 'name']
                }
                
                foods_found.append({
                    'name': cached_nutrition['name'],
                    'portion': portion,
                    'portion_text': portion_text,
                    'nutrition': portioned_nutrition,
                    'category': cached_nutrition['category'],
                    'source': 'cache'
                })
        
        # If still no matches, try Gemini AI
        if not foods_found and self.gemini_lookup:
            print(f"🤖 Using Gemini AI to lookup: {text}")
            portion, portion_text = self.parse_portion(text)
            
            # Extract just the food name (remove portion words)
            food_name = re.sub(r'\d+\.?\d*\s*(oz|ounce|cup|g|gram|serving|piece|slice)?s?', '', text).strip()
            
            gemini_nutrition = self.gemini_lookup.get_nutrition_data(food_name, portion_text)
            
            if gemini_nutrition:
                # Cache the result for future use
                if self.nutrition_cache:
                    self.nutrition_cache.set(food_name, gemini_nutrition)
                
                # Apply portion
                portioned_nutrition = {
                    k: round(v * portion, 1) 
                    for k, v in gemini_nutrition.items() 
                    if k not in ['category', 'source', 'confidence', 'name']
                }
                
                foods_found.append({
                    'name': gemini_nutrition['name'],
                    'portion': portion,
                    'portion_text': portion_text,
                    'nutrition': portioned_nutrition,
                    'category': gemini_nutrition['category'],
                    'source': 'gemini',
                    'confidence': gemini_nutrition.get('confidence', 0.85)
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
