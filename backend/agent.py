"""
Mindful Eating Agent - Supervisor-Worker Architecture
AI Agent for food parsing, nutrition analysis, and personalized recommendations
Uses a Supervisor to orchestrate specialized Workers.
"""

from typing import TypedDict, List, Dict, Any, Literal
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
    next_worker: str
    needs_ingredients: bool
    ingredient_fallback: bool
    user_message: str

# --- Supervisor Node ---
def supervisor_node(state: AgentState) -> AgentState:
    """
    The Supervisor decides which Worker to call next based on the current state.
    """
    # Error handling: if an error occurred, stop or handle it
    if state.get('error') and not state.get('ingredient_fallback'):
        state['next_worker'] = END
        return state

    # 1. If foods haven't been parsed yet, call the FoodParser Worker
    if not state.get('parsed_foods') and not state.get('needs_ingredients'):
        state['next_worker'] = 'food_parser_worker'
        return state

    # 2. If foods are parsed but nutrition isn't calculated, call Nutrition Worker
    if state.get('parsed_foods') and not state.get('nutrition_data'):
        state['next_worker'] = 'nutrition_worker'
        return state

    # 3. If nutrition is done but patterns aren't analyzed, call Analyst Worker
    if state.get('nutrition_data') and not state.get('patterns'):
        state['next_worker'] = 'pattern_analyst_worker'
        return state

    # 4. If patterns are ready but no recommendations, call Recommendation Worker
    if state.get('patterns') and not state.get('recommendations'):
        state['next_worker'] = 'recommendation_worker'
        return state

    # 5. If all tasks are complete, finish
    state['next_worker'] = END
    return state

# --- Worker Nodes ---

def food_parser_worker(state: AgentState) -> AgentState:
    """Worker 1: Specialized in parsing food text"""
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
    
    if not foods_found:
        state['needs_ingredients'] = True
        state['error'] = 'not_recognized'
        state['user_message'] = USER_PROMPTS.get('ingredient_request', 
            "I don't recognize that food. Could you tell me what ingredients are in it?")
    
    return state

def nutrition_worker(state: AgentState) -> AgentState:
    """Worker 2: Specialized in calculating nutrition totals"""
    total_nutrition = {
        'calories': sum(f['nutrition']['calories'] for f in state['parsed_foods']),
        'protein': sum(f['nutrition']['protein'] for f in state['parsed_foods']),
        'carbs': sum(f['nutrition']['carbs'] for f in state['parsed_foods']),
        'fat': sum(f['nutrition']['fat'] for f in state['parsed_foods']),
        'fiber': sum(f['nutrition']['fiber'] for f in state['parsed_foods']),
    }
    
    state['nutrition_data'] = total_nutrition
    return state

def pattern_analyst_worker(state: AgentState) -> AgentState:
    """Worker 3: Specialized in analyzing user history"""
    user_history = state.get('user_history', [])
    patterns = recommendation_engine.analyze_patterns(user_history)
    state['patterns'] = patterns
    return state

def recommendation_worker(state: AgentState) -> AgentState:
    """Worker 4: Specialized in generating advice"""
    nutrition_data = state.get('nutrition_data', {})
    user_history = state.get('user_history', [])
    patterns = state.get('patterns', {})
    
    recommendations = recommendation_engine.generate_recommendations(
        nutrition_data,
        user_history,
        patterns
    )
    
    state['recommendations'] = recommendations
    return state

def route_from_supervisor(state: AgentState) -> Literal['food_parser_worker', 'nutrition_worker', 'pattern_analyst_worker', 'recommendation_worker', END]:
    """Router function for the Supervisor"""
    return state['next_worker']

# Build the Supervisor-Worker Graph
def create_mindful_eating_agent():
    """Create the LangGraph agent workflow with Supervisor architecture"""
    
    workflow = StateGraph(AgentState)
    
    # Add Supervisor and Workers
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("food_parser_worker", food_parser_worker)
    workflow.add_node("nutrition_worker", nutrition_worker)
    workflow.add_node("pattern_analyst_worker", pattern_analyst_worker)
    workflow.add_node("recommendation_worker", recommendation_worker)
    
    # Set entry point
    workflow.set_entry_point("supervisor")
    
    # Supervisor Routing Logic
    workflow.add_conditional_edges(
        "supervisor",
        route_from_supervisor
    )
    
    # Workers always report back to Supervisor
    workflow.add_edge("food_parser_worker", "supervisor")
    workflow.add_edge("nutrition_worker", "supervisor")
    workflow.add_edge("pattern_analyst_worker", "supervisor")
    workflow.add_edge("recommendation_worker", "supervisor")
    
    # Compile the graph
    app = workflow.compile()
    
    return app

# Create the agent instance
mindful_eating_agent = create_mindful_eating_agent()

def process_food_log(user_id: str, food_text: str, meal_type: str, user_history: List[Dict]) -> Dict:
    """
    Process food log using the Supervisor-Worker Agent
    
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
        'next_worker': '',
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
