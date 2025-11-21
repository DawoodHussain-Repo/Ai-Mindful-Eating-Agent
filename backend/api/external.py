"""
External API Interface for Mindful Eating Agent
Allows the agent to be called by external supervisors or systems
Production-grade with proper error handling and validation
"""

from flask import Blueprint, request, jsonify
from agent import process_food_log
from utils.mongodb_client import MongoDBClient, FoodLogOperations
import os

# Create Blueprint for external API
external_api = Blueprint('external_api', __name__, url_prefix='/api/v1/agent')

# Initialize MongoDB client
try:
    mongo_client = MongoDBClient()
    food_log_ops = FoodLogOperations(mongo_client)
except Exception as e:
    print(f"Warning: MongoDB not available for external API: {e}")
    mongo_client = None
    food_log_ops = None

@external_api.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint for supervisor systems
    Returns system status and availability
    """
    db_status = "connected" if mongo_client else "disconnected"
    
    return jsonify({
        "status": "healthy",
        "service": "Mindful Eating Agent",
        "version": "1.0.0",
        "architecture": "Supervisor-Worker (LangGraph)",
        "database": db_status,
        "capabilities": [
            "food_parsing",
            "nutrition_calculation",
            "pattern_analysis",
            "recommendations"
        ]
    }), 200

@external_api.route('/process', methods=['POST'])
def process_food_external():
    """
    External endpoint for processing food logs
    
    Request JSON:
    {
        "user_id": "string",
        "food_text": "string",
        "meal_type": "breakfast|lunch|dinner|snack",
        "user_history": [...]  // optional
    }
    
    Response JSON:
    {
        "success": boolean,
        "foods": [...],
        "total_nutrition": {...},
        "recommendations": [...],
        "user_message": "string",
        "needs_clarification": boolean,
        "clarification_question": "string"  // if needs_clarification
    }
    """
    try:
        # Validate request
        data = request.get_json()
        
        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data provided"
            }), 400
        
        # Required fields
        user_id = data.get('user_id')
        food_text = data.get('food_text')
        meal_type = data.get('meal_type', 'snack')
        
        if not user_id or not food_text:
            return jsonify({
                "success": False,
                "error": "Missing required fields: user_id and food_text"
            }), 400
        
        # Validate meal_type
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if meal_type not in valid_meal_types:
            return jsonify({
                "success": False,
                "error": f"Invalid meal_type. Must be one of: {', '.join(valid_meal_types)}"
            }), 400
        
        # Get user history (optional)
        user_history = data.get('user_history', [])
        
        # If no history provided and MongoDB is available, fetch from DB
        if not user_history and food_log_ops:
            try:
                user_history = food_log_ops.get_recent_logs(user_id, days=14)
            except Exception as e:
                print(f"Could not fetch user history: {e}")
                user_history = []
        
        # Process using the agent
        result = process_food_log(
            user_id=user_id,
            food_text=food_text,
            meal_type=meal_type,
            user_history=user_history
        )
        
        # Return result
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Internal server error: {str(e)}"
        }), 500

@external_api.route('/schema', methods=['GET'])
def get_api_schema():
    """
    Returns the API contract/schema for integration
    """
    schema = {
        "api_version": "1.0.0",
        "base_url": "/api/v1/agent",
        "endpoints": {
            "/health": {
                "method": "GET",
                "description": "Health check endpoint",
                "response": {
                    "status": "string",
                    "service": "string",
                    "version": "string",
                    "architecture": "string",
                    "database": "string",
                    "capabilities": ["array of strings"]
                }
            },
            "/process": {
                "method": "POST",
                "description": "Process food log and return nutrition analysis",
                "request": {
                    "user_id": "string (required)",
                    "food_text": "string (required)",
                    "meal_type": "string (required: breakfast|lunch|dinner|snack)",
                    "user_history": "array (optional)"
                },
                "response": {
                    "success": "boolean",
                    "foods": "array of food objects",
                    "total_nutrition": "object with calories, protein, carbs, fat, fiber",
                    "recommendations": "array of recommendation objects",
                    "user_message": "string",
                    "needs_clarification": "boolean",
                    "clarification_question": "string (if needs_clarification)"
                }
            },
            "/schema": {
                "method": "GET",
                "description": "Get API contract/schema",
                "response": "This schema document"
            }
        },
        "example_request": {
            "user_id": "user123",
            "food_text": "I had grilled chicken and rice for dinner",
            "meal_type": "dinner"
        },
        "example_response": {
            "success": True,
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
                },
                {
                    "name": "Rice",
                    "portion": 1.0,
                    "portion_text": "1 serving",
                    "nutrition": {
                        "calories": 205,
                        "protein": 4.3,
                        "carbs": 45,
                        "fat": 0.4,
                        "fiber": 0.6
                    },
                    "category": "carbs"
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
                    "message": "Great protein choice! You're on track."
                }
            ],
            "user_message": "Great choice! Grilled Chicken is packed with protein. 💪",
            "needs_clarification": False
        }
    }
    
    return jsonify(schema), 200

# Export blueprint
__all__ = ['external_api']
