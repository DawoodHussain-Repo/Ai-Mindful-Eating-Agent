"""
Conversational Food Logging Agent - Enhanced LangGraph Implementation
Handles misspellings, unknown foods, and conversational interactions
"""

from typing import TypedDict, List, Dict, Any, Optional
from langgraph.graph import StateGraph, END
from datetime import datetime
import re
from difflib import get_close_matches

# Import utilities
from utils.data_loader import load_food_database, load_user_prompts
from utils.food_parser import FoodParser
from utils.recommendation_engine import RecommendationEngine

# Load configurations
FOOD_DATABASE = load_food_database()
USER_PROMPTS = load_user_prompts()

# Define portion patterns and sizes
PORTION_PATTERNS = {
    'oz': r'(\d+\.?\d*)\s*(?:oz|ounce|ounces)',
    'cup': r'(\d+\.?\d*|1/2|1/4|half|quarter)\s*(?:cup|cups)',
    'gram': r'(\d+\.?\d*)\s*(?:g|gram|grams)',
    'piece': r'(\d+\.?\d*)\s*(?:piece|pieces|slice|slices)',
    'serving': r'(\d+\.?\d*)\s*(?:serving|servings)',
}

PORTION_SIZES = {
    'small': 0.75,
    'medium': 1.0,
    'large': 1.5,
    'huge': 2.0,
}

# Define nutrition thresholds
NUTRITION_THRESHOLDS = {
    'low_protein': 60,
    'good_protein': 80,
    'target_protein': 120,
    'low_calories': 1200,
    'target_calories': 2000,
    'high_calories': 2200,
    'food_frequency_alert': 3,
}

# Initialize utilities
food_parser = FoodParser(FOOD_DATABASE, PORTION_PATTERNS, PORTION_SIZES)
recommendation_engine = RecommendationEngine(NUTRITION_THRESHOLDS, USER_PROMPTS)

# Define the Conversational Agent State
class ConversationalAgentState(TypedDict):
    """State for the Conversational Food Logging Agent"""
    user_id: str
    user_message: str
    conversation_history: List[Dict[str, str]]
    intent: str  # 'log_food', 'ask_question', 'unclear', 'greeting'
    parsed_foods: List[Dict[str, Any]]
    unknown_foods: List[str]
    suggestions: List[Dict[str, Any]]
    nutrition_data: Dict[str, float]
    user_history: List[Dict[str, Any]]
    recommendations: List[Dict[str, str]]
    agent_response: str
    needs_clarification: bool
    clarification_question: str
    confidence: float
    step: str

# Agent Node Functions

def detect_intent_node(state: ConversationalAgentState) -> ConversationalAgentState:
    """Node 1: Detect user intent from message"""
    message = state['user_message'].lower().strip()
    
    # Greeting patterns
    greetings = ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening']
    if any(greeting in message for greeting in greetings):
        state['intent'] = 'greeting'
        state['agent_response'] = "Hey! 👋 What did you eat? Just tell me naturally, like you're texting a friend!"
        state['step'] = 'complete'
        return state
    
    # Question patterns
    question_words = ['what', 'how', 'why', 'when', 'can', 'should', 'is', '?']
    if any(word in message for word in question_words) and 'ate' not in message and 'had' not in message:
        state['intent'] = 'ask_question'
        state['agent_response'] = "I'm here to help you log your meals! Just tell me what you ate, and I'll track the nutrition for you. 😊"
        state['step'] = 'complete'
        return state
    
    # Food logging intent (default)
    state['intent'] = 'log_food'
    state['step'] = 'intent_detected'
    return state

def calculate_from_ingredients(ingredients_text: str) -> Dict[str, Any]:
    """Calculate nutrition from a list of ingredients"""
    ingredients = re.split(r'[,;]|\band\b', ingredients_text.lower())
    all_food_names = list(FOOD_DATABASE.keys())
    
    total_nutrition = {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0,
        'fiber': 0
    }
    
    found_ingredients = []
    
    for ingredient in ingredients:
        ingredient = ingredient.strip()
        if not ingredient or len(ingredient) < 3:
            continue
        
        # Try exact match
        matched = False
        for food_name in all_food_names:
            if food_name in ingredient or ingredient in food_name:
                nutrition = FOOD_DATABASE[food_name]
                # Use smaller portions for ingredients (0.5 serving)
                for key in total_nutrition:
                    if key in nutrition:
                        total_nutrition[key] += nutrition[key] * 0.5
                found_ingredients.append(food_name.title())
                matched = True
                break
        
        # Try fuzzy match if no exact match
        if not matched:
            close_matches = get_close_matches(ingredient, all_food_names, n=1, cutoff=0.6)
            if close_matches:
                food_name = close_matches[0]
                nutrition = FOOD_DATABASE[food_name]
                for key in total_nutrition:
                    if key in nutrition:
                        total_nutrition[key] += nutrition[key] * 0.5
                found_ingredients.append(food_name.title())
    
    return {
        'success': len(found_ingredients) > 0,
        'ingredients': found_ingredients,
        'nutrition': {k: round(v, 1) for k, v in total_nutrition.items()}
    }

def parse_conversational_food_node(state: ConversationalAgentState) -> ConversationalAgentState:
    """Node 2: Parse food from conversational text with fuzzy matching"""
    if state['intent'] != 'log_food':
        return state
    
    message = state['user_message'].lower()
    
    # Check if this is a response to ingredient request
    if state.get('unknown_foods') and any(word in message for word in ['yes', 'yeah', 'yep', 'sure', 'ok']):
        # User confirmed the suggestion, use previous unknown food
        state['needs_clarification'] = False
        state['step'] = 'parsed'
        return state
    
    # Check if user is providing ingredients (contains multiple food items separated by commas)
    if ',' in message or ' and ' in message:
        ingredient_result = calculate_from_ingredients(message)
        if ingredient_result['success']:
            # Create a combined food entry from ingredients
            foods_found = [{
                'name': 'Mixed Dish',
                'portion': 1.0,
                'portion_text': '1 serving (from ingredients)',
                'nutrition': ingredient_result['nutrition'],
                'category': 'mixed',
                'confidence': 0.8,
                'ingredients': ingredient_result['ingredients']
            }]
            state['parsed_foods'] = foods_found
            state['needs_clarification'] = False
            state['step'] = 'parsed'
            return state
    
    message = state['user_message'].lower()
    
    # Extract food items with fuzzy matching
    foods_found = []
    unknown_foods = []
    all_food_names = list(FOOD_DATABASE.keys())
    
    # Common conversational patterns
    message = re.sub(r'\b(i ate|i had|just ate|just had|for (breakfast|lunch|dinner|snack))\b', '', message)
    message = re.sub(r'\b(some|a|an|the)\b', '', message)
    
    # Split by common separators
    potential_foods = re.split(r'[,;]|\band\b|\bwith\b', message)
    
    for food_text in potential_foods:
        food_text = food_text.strip()
        if not food_text or len(food_text) < 3:
            continue
        
        # Try exact match first
        matched = False
        for food_name in all_food_names:
            if food_name in food_text:
                # Extract portion if present
                portion_match = re.search(r'(\d+\.?\d*)\s*(oz|ounce|ounces|cup|cups|g|gram|grams|serving|servings)?', food_text)
                portion = 1.0
                portion_text = "1 serving"
                
                if portion_match:
                    amount = float(portion_match.group(1))
                    unit = portion_match.group(2) or 'serving'
                    
                    if 'oz' in unit or 'ounce' in unit:
                        portion = amount / 4
                        portion_text = f"{amount} oz"
                    elif 'cup' in unit:
                        portion = amount
                        portion_text = f"{amount} cup"
                    elif 'g' in unit or 'gram' in unit:
                        portion = amount / 100
                        portion_text = f"{amount}g"
                    else:
                        portion = amount
                        portion_text = f"{amount} serving"
                
                nutrition = FOOD_DATABASE[food_name]
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
                    'confidence': 1.0
                })
                matched = True
                break
        
        # If no exact match, try fuzzy matching
        if not matched:
            # Extract main food word (remove numbers and units)
            food_word = re.sub(r'\d+\.?\d*\s*(oz|ounce|cup|g|gram|serving)?', '', food_text).strip()
            
            if food_word:
                # Find close matches
                close_matches = get_close_matches(food_word, all_food_names, n=3, cutoff=0.6)
                
                if close_matches:
                    # Use the best match
                    best_match = close_matches[0]
                    nutrition = FOOD_DATABASE[best_match]
                    
                    foods_found.append({
                        'name': best_match.title(),
                        'portion': 1.0,
                        'portion_text': '1 serving (estimated)',
                        'nutrition': {k: v for k, v in nutrition.items() if k != 'category'},
                        'category': nutrition['category'],
                        'confidence': 0.7,
                        'original_text': food_word,
                        'suggestions': [m.title() for m in close_matches]
                    })
                else:
                    unknown_foods.append(food_word)
    
    state['parsed_foods'] = foods_found
    state['unknown_foods'] = unknown_foods
    
    # Determine if clarification is needed
    if not foods_found and unknown_foods:
        state['needs_clarification'] = True
        unknown_food = unknown_foods[0]
        state['clarification_question'] = f"I don't recognize '{unknown_food}' 🤔\n\nCan you tell me what ingredients are in it? (e.g., 'bread, cheese, meat, tomato')\n\nOr try describing it differently!"
        state['unknown_foods'] = unknown_foods
        state['step'] = 'needs_clarification'
    elif foods_found and any(f['confidence'] < 0.9 for f in foods_found):
        # Low confidence matches
        low_conf_foods = [f for f in foods_found if f['confidence'] < 0.9]
        suggestions_text = ', '.join([f"'{f['name']}'" for f in low_conf_foods])
        state['needs_clarification'] = True
        state['clarification_question'] = f"Did you mean {suggestions_text}? 🤔\n\n(Reply 'yes' to confirm or tell me what you actually meant)"
        state['step'] = 'needs_clarification'
    else:
        state['needs_clarification'] = False
        state['step'] = 'parsed'
    
    return state

def calculate_nutrition_node(state: ConversationalAgentState) -> ConversationalAgentState:
    """Node 3: Calculate total nutrition"""
    if state['intent'] != 'log_food' or state['needs_clarification']:
        return state
    
    if not state['parsed_foods']:
        state['agent_response'] = "I couldn't find any foods in your message. Try something like: 'I had chicken and rice' or 'ate a burger'"
        state['step'] = 'complete'
        return state
    
    total_nutrition = {
        'calories': sum(f['nutrition']['calories'] for f in state['parsed_foods']),
        'protein': sum(f['nutrition']['protein'] for f in state['parsed_foods']),
        'carbs': sum(f['nutrition']['carbs'] for f in state['parsed_foods']),
        'fat': sum(f['nutrition']['fat'] for f in state['parsed_foods']),
        'fiber': sum(f['nutrition']['fiber'] for f in state['parsed_foods']),
    }
    
    state['nutrition_data'] = total_nutrition
    state['step'] = 'nutrition_calculated'
    
    return state

def generate_conversational_response_node(state: ConversationalAgentState) -> ConversationalAgentState:
    """Node 4: Generate friendly, conversational response"""
    if state['intent'] != 'log_food' or state['needs_clarification']:
        return state
    
    foods = state['parsed_foods']
    nutrition = state['nutrition_data']
    
    # Build conversational response
    food_list = ', '.join([f"{f['name']} ({f['portion_text']})" for f in foods])
    
    responses = [
        f"Got it! Logged: {food_list} 📝",
        f"Nice! I tracked: {food_list} ✅",
        f"Awesome! Added: {food_list} 🍽️",
        f"Perfect! Logged: {food_list} 👍"
    ]
    
    import random
    response = random.choice(responses)
    
    # If this was calculated from ingredients, mention it
    if foods and 'ingredients' in foods[0]:
        ingredients_list = ', '.join(foods[0]['ingredients'])
        response += f"\n\n🧩 Ingredients detected: {ingredients_list}"
    
    # Add nutrition summary
    response += f"\n\n📊 Nutrition Summary:\n"
    response += f"• {round(nutrition['calories'])} calories\n"
    response += f"• {round(nutrition['protein'])}g protein\n"
    response += f"• {round(nutrition['carbs'])}g carbs\n"
    response += f"• {round(nutrition['fat'])}g fat"
    
    # Add contextual comment
    if nutrition['protein'] > 30:
        response += "\n\n💪 Great protein intake!"
    elif nutrition['calories'] > 600:
        response += "\n\n🔥 That's a solid meal!"
    elif nutrition['fiber'] > 5:
        response += "\n\n🥗 Nice fiber content!"
    
    state['agent_response'] = response
    state['step'] = 'nutrition_calculated'
    
    return state

def generate_recommendations_node(state: ConversationalAgentState) -> ConversationalAgentState:
    """Node 5: Generate recommendations based on history"""
    if state['intent'] != 'log_food' or state['needs_clarification']:
        return state
    
    user_history = state.get('user_history', [])
    nutrition_data = state.get('nutrition_data', {})
    
    # Analyze patterns from history
    patterns = {}
    if user_history:
        recent_logs = user_history[-14:]  # Last 2 weeks
        food_frequency = {}
        for log in recent_logs:
            for food in log.get('foods', []):
                food_name = food.get('name', '')
                food_frequency[food_name] = food_frequency.get(food_name, 0) + 1
        patterns['food_frequency'] = food_frequency
    
    recommendations = recommendation_engine.generate_recommendations(
        nutrition_data,
        user_history,
        patterns
    )
    
    state['recommendations'] = recommendations
    state['step'] = 'complete'
    
    return state

def should_continue(state: ConversationalAgentState) -> str:
    """Determine next step in the workflow"""
    step = state.get('step', '')
    
    if step == 'complete':
        return END
    elif step == 'intent_detected':
        return 'parse_food'
    elif step == 'needs_clarification':
        return END
    elif step == 'parsed':
        return 'calculate_nutrition'
    elif step == 'nutrition_calculated':
        return 'generate_recommendations'
    elif step == 'recommendations_generated':
        return END
    
    return END

# Build the Conversational LangGraph Agent
def create_conversational_agent():
    """Create the conversational LangGraph agent workflow"""
    
    workflow = StateGraph(ConversationalAgentState)
    
    # Add nodes
    workflow.add_node("detect_intent", detect_intent_node)
    workflow.add_node("parse_food", parse_conversational_food_node)
    workflow.add_node("calculate_nutrition", calculate_nutrition_node)
    workflow.add_node("generate_response", generate_conversational_response_node)
    workflow.add_node("generate_recommendations", generate_recommendations_node)
    
    # Set entry point
    workflow.set_entry_point("detect_intent")
    
    # Add edges
    workflow.add_conditional_edges(
        "detect_intent",
        should_continue,
        {
            "parse_food": "parse_food",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "parse_food",
        should_continue,
        {
            "calculate_nutrition": "calculate_nutrition",
            END: END
        }
    )
    
    workflow.add_edge("calculate_nutrition", "generate_response")
    workflow.add_edge("generate_response", "generate_recommendations")
    workflow.add_edge("generate_recommendations", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# Create the agent instance
conversational_agent = create_conversational_agent()

def process_conversational_message(
    user_id: str, 
    message: str, 
    conversation_history: List[Dict[str, str]],
    user_history: List[Dict]
) -> Dict:
    """
    Process a conversational message from the user
    
    Args:
        user_id: User identifier
        message: User's message
        conversation_history: Previous conversation messages
        user_history: User's meal history
    
    Returns:
        Dict with agent response, parsed foods, and recommendations
    """
    
    initial_state = {
        'user_id': user_id,
        'user_message': message,
        'conversation_history': conversation_history,
        'intent': '',
        'parsed_foods': [],
        'unknown_foods': [],
        'suggestions': [],
        'nutrition_data': {},
        'user_history': user_history,
        'recommendations': [],
        'agent_response': '',
        'needs_clarification': False,
        'clarification_question': '',
        'confidence': 1.0,
        'step': 'initial'
    }
    
    # Run the agent
    result = conversational_agent.invoke(initial_state)
    
    return {
        'success': result['intent'] == 'log_food' and not result['needs_clarification'],
        'agent_response': result.get('agent_response', ''),
        'foods': result.get('parsed_foods', []),
        'total_nutrition': result.get('nutrition_data', {}),
        'recommendations': result.get('recommendations', []),
        'needs_clarification': result.get('needs_clarification', False),
        'clarification_question': result.get('clarification_question', ''),
        'intent': result.get('intent', 'log_food')
    }