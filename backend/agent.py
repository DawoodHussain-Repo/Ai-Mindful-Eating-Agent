"""
Mindful Eating Agent - LangGraph Implementation (Refactored)
AI Agent for food parsing, nutrition analysis, and personalized recommendations
Uses JSON configuration files for better maintainability
"""

from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END
from datetime import datetime

# Import utilities
from utils.data_loader import (
    load_food_database,
    load_user_prompts,
    load_app_config,
    load_nutrition_goals
)
from utils.food_parser import FoodParser
from utils.recommendation_engine import RecommendationEngine

# Load configurations
FOOD_DATABASE = load_food_database()
USER_PROMPTS = load_user_prompts()
APP_CONFIG = load_app_config()
NUTRITION_GOALS = load_nutrition_goals()

# Initialize utilities
food_parser = FoodParser(
    FOOD_DATABASE,
    APP_CONFIG.get('portion_patterns', {}),
    APP_CONFIG.get('portion_sizes', {})
)

recommendation_engine = RecommendationEngine(
    APP_CONFIG.get('recommendation_thresholds', {}),
    USER_PROMPTS
)

# Define the Agent State
class AgentState(TypedDict):
    """State for the Mindful Eating Agent"""
    user_id: str
    input_text: str
    meal_type: str
    parsed_foods: List[Dict[str, Any]]
    nutrition_data: Dict[str, float]
    user_history: List[Dict[str, Any]]
    patterns: Dict[str, Any]
    recommendations: List[Dict[str, str]]
    error: str
    step: str
    needs_ingredients: bool
    ingredient_fallback: bool
    user_message: str

# Agent Node Functions
def parse_food_node(state: AgentState) -> AgentState:
    """Node 1: Parse food text using NLP with ingredient fallback"""
    text = state['input_text']
    
    # Parse using FoodParser utility
    foods_found = food_parser.parse_food_text(text)
    
    # If no exact matches, try ingredient-based estimation
    if not foods_found:
        ingredient_result = food_parser.estimate_from_ingredients(text)
        if ingredient_result['success']:
            foods_found.append({
                'name': 'Mixed Dish (estimated)',
                'portion': 1.0,
                'portion_text': '1 serving (estimated)',
                'nutrition': ingredient_result['nutrition'],
                'category': 'mixed',
                'estimated': True,
                'ingredients': ingredient_result['ingredients']
            })
            state['ingredient_fallback'] = True
            state['user_message'] = USER_PROMPTS.get('estimated', '').format(
                ingredients=', '.join(ingredient_result['ingredients'])
            )
    
    state['parsed_foods'] = foods_found
    state['step'] = 'parsed'
    
    if not foods_found:
        state['needs_ingredients'] = True
        state['error'] = 'not_recognized'
        state['user_message'] = USER_PROMPTS.get('ingredient_request', 
            "I don't recognize that food. Could you tell me what ingredients are in it?")
    
    return state

def calculate_nutrition_node(state: AgentState) -> AgentState:
    """Node 2: Calculate total nutrition"""
    if state.get('error') and not state.get('ingredient_fallback'):
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

def analyze_patterns_node(state: AgentState) -> AgentState:
    """Node 3: Analyze eating patterns"""
    if state.get('error') and not state.get('ingredient_fallback'):
        return state
    
    user_history = state.get('user_history', [])
    
    # Use recommendation engine to analyze patterns
    patterns = recommendation_engine.analyze_patterns(user_history)
    
    state['patterns'] = patterns
    state['step'] = 'patterns_analyzed'
    
    return state

def generate_recommendations_node(state: AgentState) -> AgentState:
    """Node 4: Generate personalized, friendly recommendations"""
    if state.get('error') and not state.get('ingredient_fallback'):
        return state
    
    nutrition_data = state.get('nutrition_data', {})
    user_history = state.get('user_history', [])
    patterns = state.get('patterns', {})
    
    # Use recommendation engine to generate recommendations
    recommendations = recommendation_engine.generate_recommendations(
        nutrition_data,
        user_history,
        patterns
    )
    
    state['recommendations'] = recommendations
    state['step'] = 'recommendations_generated'
    
    return state

def should_continue(state: AgentState) -> str:
    """Determine if agent should continue or end"""
    if state.get('error') and not state.get('ingredient_fallback'):
        return END
    
    step = state.get('step', '')
    
    if step == 'parsed':
        return 'calculate_nutrition'
    elif step == 'nutrition_calculated':
        return 'analyze_patterns'
    elif step == 'patterns_analyzed':
        return 'generate_recommendations'
    elif step == 'recommendations_generated':
        return END
    
    return END

# Build the LangGraph Agent
def create_mindful_eating_agent():
    """Create the LangGraph agent workflow"""
    
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("parse_food", parse_food_node)
    workflow.add_node("calculate_nutrition", calculate_nutrition_node)
    workflow.add_node("analyze_patterns", analyze_patterns_node)
    workflow.add_node("generate_recommendations", generate_recommendations_node)
    
    # Set entry point
    workflow.set_entry_point("parse_food")
    
    # Add edges
    workflow.add_conditional_edges(
        "parse_food",
        should_continue,
        {
            "calculate_nutrition": "calculate_nutrition",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "calculate_nutrition",
        should_continue,
        {
            "analyze_patterns": "analyze_patterns",
            END: END
        }
    )
    
    workflow.add_conditional_edges(
        "analyze_patterns",
        should_continue,
        {
            "generate_recommendations": "generate_recommendations",
            END: END
        }
    )
    
    workflow.add_edge("generate_recommendations", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# Create the agent instance
mindful_eating_agent = create_mindful_eating_agent()

def process_food_log(user_id: str, food_text: str, meal_type: str, user_history: List[Dict]) -> Dict:
    """
    Process food log using the LangGraph agent
    
    Args:
        user_id: User identifier
        food_text: Text description of food
        meal_type: Type of meal (breakfast, lunch, dinner, snack)
        user_history: User's meal history
    
    Returns:
        Dict with parsed foods, nutrition, and recommendations
    """
    
    initial_state = {
        'user_id': user_id,
        'input_text': food_text,
        'meal_type': meal_type,
        'parsed_foods': [],
        'nutrition_data': {},
        'user_history': user_history,
        'patterns': {},
        'recommendations': [],
        'error': '',
        'step': 'initial',
        'needs_ingredients': False,
        'ingredient_fallback': False,
        'user_message': ''
    }
    
    # Run the agent
    result = mindful_eating_agent.invoke(initial_state)
    
    return {
        'success': not result.get('error') or result.get('ingredient_fallback'),
        'error': result.get('error'),
        'foods': result.get('parsed_foods', []),
        'total_nutrition': result.get('nutrition_data', {}),
        'recommendations': result.get('recommendations', []),
        'patterns': result.get('patterns', {}),
        'user_message': result.get('user_message', ''),
        'needs_ingredients': result.get('needs_ingredients', False)
    }
