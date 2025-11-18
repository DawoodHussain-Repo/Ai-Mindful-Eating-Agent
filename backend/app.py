"""
Mindful Eating Agent - Flask Backend
Text-based food logging with AI-powered nutrition analysis using LangGraph
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
import re

# Import LangGraph Agents
from agent import process_food_log, mindful_eating_agent
from agent_chat import process_conversational_message

# Import MongoDB utilities
from utils.mongodb_client import (
    MongoDBClient, 
    UserOperations, 
    FoodLogOperations,
    SessionOperations
)

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Enable CORS for Next.js frontend
CORS(app, supports_credentials=True, origins=['http://localhost:3000'])

# MongoDB Session Configuration
app.config['SESSION_TYPE'] = 'mongodb'
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_KEY_PREFIX'] = 'mindful_eating:'

# Initialize MongoDB
try:
    mongo_client = MongoDBClient('config/mongodb_config.json')
    app.config['SESSION_MONGODB'] = mongo_client.client
    app.config['SESSION_MONGODB_DB'] = mongo_client.db.name
    app.config['SESSION_MONGODB_COLLECT'] = 'sessions'
    
    # Initialize database operations
    user_ops = UserOperations(mongo_client)
    food_log_ops = FoodLogOperations(mongo_client)
    session_ops = SessionOperations(mongo_client)
    
    print("✅ MongoDB initialized successfully")
except Exception as e:
    print(f"❌ Failed to initialize MongoDB: {e}")
    print("Please ensure MongoDB is running on localhost:27017")
    exit(1)

# Initialize Flask-Session
Session(app)

# Comprehensive nutritional database
FOOD_DATABASE = {
    # Proteins
    'chicken breast': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'grilled chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'chicken': {'calories': 165, 'protein': 31, 'carbs': 0, 'fat': 3.6, 'fiber': 0, 'category': 'protein'},
    'salmon': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 13, 'fiber': 0, 'category': 'protein'},
    'fish': {'calories': 206, 'protein': 22, 'carbs': 0, 'fat': 13, 'fiber': 0, 'category': 'protein'},
    'tuna': {'calories': 132, 'protein': 28, 'carbs': 0, 'fat': 1.3, 'fiber': 0, 'category': 'protein'},
    'beef': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0, 'category': 'protein'},
    'steak': {'calories': 250, 'protein': 26, 'carbs': 0, 'fat': 15, 'fiber': 0, 'category': 'protein'},
    'turkey': {'calories': 135, 'protein': 30, 'carbs': 0, 'fat': 0.7, 'fiber': 0, 'category': 'protein'},
    'pork': {'calories': 242, 'protein': 27, 'carbs': 0, 'fat': 14, 'fiber': 0, 'category': 'protein'},
    'eggs': {'calories': 155, 'protein': 13, 'carbs': 1.1, 'fat': 11, 'fiber': 0, 'category': 'protein'},
    'egg': {'calories': 78, 'protein': 6.5, 'carbs': 0.6, 'fat': 5.5, 'fiber': 0, 'category': 'protein'},
    'tofu': {'calories': 76, 'protein': 8, 'carbs': 1.9, 'fat': 4.8, 'fiber': 0.3, 'category': 'protein'},
    
    # Carbs
    'brown rice': {'calories': 216, 'protein': 5, 'carbs': 45, 'fat': 1.8, 'fiber': 3.5, 'category': 'carbs'},
    'white rice': {'calories': 205, 'protein': 4.3, 'carbs': 45, 'fat': 0.4, 'fiber': 0.6, 'category': 'carbs'},
    'rice': {'calories': 205, 'protein': 4.3, 'carbs': 45, 'fat': 0.4, 'fiber': 0.6, 'category': 'carbs'},
    'quinoa': {'calories': 222, 'protein': 8, 'carbs': 39, 'fat': 3.6, 'fiber': 5.2, 'category': 'carbs'},
    'pasta': {'calories': 221, 'protein': 8, 'carbs': 43, 'fat': 1.3, 'fiber': 2.5, 'category': 'carbs'},
    'bread': {'calories': 265, 'protein': 9, 'carbs': 49, 'fat': 3.2, 'fiber': 2.7, 'category': 'carbs'},
    'toast': {'calories': 79, 'protein': 2.6, 'carbs': 15, 'fat': 1, 'fiber': 0.8, 'category': 'carbs'},
    'bagel': {'calories': 289, 'protein': 11, 'carbs': 56, 'fat': 2, 'fiber': 2.3, 'category': 'carbs'},
    'oatmeal': {'calories': 158, 'protein': 6, 'carbs': 27, 'fat': 3.2, 'fiber': 4, 'category': 'carbs'},
    'potato': {'calories': 163, 'protein': 4.3, 'carbs': 37, 'fat': 0.2, 'fiber': 2.5, 'category': 'carbs'},
    'sweet potato': {'calories': 180, 'protein': 4, 'carbs': 41, 'fat': 0.3, 'fiber': 6.6, 'category': 'carbs'},
    
    # Vegetables
    'broccoli': {'calories': 55, 'protein': 3.7, 'carbs': 11, 'fat': 0.6, 'fiber': 2.4, 'category': 'vegetables'},
    'spinach': {'calories': 23, 'protein': 2.9, 'carbs': 3.6, 'fat': 0.4, 'fiber': 2.2, 'category': 'vegetables'},
    'carrots': {'calories': 41, 'protein': 0.9, 'carbs': 10, 'fat': 0.2, 'fiber': 2.8, 'category': 'vegetables'},
    'tomato': {'calories': 18, 'protein': 0.9, 'carbs': 3.9, 'fat': 0.2, 'fiber': 1.2, 'category': 'vegetables'},
    'lettuce': {'calories': 15, 'protein': 1.4, 'carbs': 2.9, 'fat': 0.2, 'fiber': 1.3, 'category': 'vegetables'},
    'cucumber': {'calories': 16, 'protein': 0.7, 'carbs': 3.6, 'fat': 0.1, 'fiber': 0.5, 'category': 'vegetables'},
    'bell pepper': {'calories': 31, 'protein': 1, 'carbs': 6, 'fat': 0.3, 'fiber': 2.1, 'category': 'vegetables'},
    'onion': {'calories': 40, 'protein': 1.1, 'carbs': 9.3, 'fat': 0.1, 'fiber': 1.7, 'category': 'vegetables'},
    'mushroom': {'calories': 22, 'protein': 3.1, 'carbs': 3.3, 'fat': 0.3, 'fiber': 1, 'category': 'vegetables'},
    
    # Dairy
    'milk': {'calories': 149, 'protein': 8, 'carbs': 12, 'fat': 8, 'fiber': 0, 'category': 'dairy'},
    'cheese': {'calories': 402, 'protein': 25, 'carbs': 1.3, 'fat': 33, 'fiber': 0, 'category': 'dairy'},
    'yogurt': {'calories': 59, 'protein': 10, 'carbs': 3.6, 'fat': 0.4, 'fiber': 0, 'category': 'dairy'},
    'greek yogurt': {'calories': 100, 'protein': 17, 'carbs': 6, 'fat': 0.7, 'fiber': 0, 'category': 'dairy'},
    'cream cheese': {'calories': 99, 'protein': 2, 'carbs': 1.6, 'fat': 10, 'fiber': 0, 'category': 'dairy'},
    
    # Fast Food / Treats
    'pizza': {'calories': 285, 'protein': 12, 'carbs': 36, 'fat': 10, 'fiber': 2.5, 'category': 'fast_food'},
    'burger': {'calories': 354, 'protein': 20, 'carbs': 30, 'fat': 17, 'fiber': 1.5, 'category': 'fast_food'},
    'fries': {'calories': 312, 'protein': 3.4, 'carbs': 41, 'fat': 15, 'fiber': 3.8, 'category': 'fast_food'},
    'donut': {'calories': 269, 'protein': 3, 'carbs': 31, 'fat': 15, 'fiber': 0.9, 'category': 'treats'},
    'cookie': {'calories': 142, 'protein': 2, 'carbs': 20, 'fat': 6.5, 'fiber': 0.7, 'category': 'treats'},
    'ice cream': {'calories': 207, 'protein': 3.5, 'carbs': 24, 'fat': 11, 'fiber': 0.7, 'category': 'treats'},
    
    # Fruits
    'apple': {'calories': 95, 'protein': 0.5, 'carbs': 25, 'fat': 0.3, 'fiber': 4.4, 'category': 'fruits'},
    'banana': {'calories': 105, 'protein': 1.3, 'carbs': 27, 'fat': 0.4, 'fiber': 3.1, 'category': 'fruits'},
    'orange': {'calories': 62, 'protein': 1.2, 'carbs': 15, 'fat': 0.2, 'fiber': 3.1, 'category': 'fruits'},
    'berries': {'calories': 57, 'protein': 1.1, 'carbs': 14, 'fat': 0.5, 'fiber': 2.4, 'category': 'fruits'},
    'strawberry': {'calories': 32, 'protein': 0.7, 'carbs': 7.7, 'fat': 0.3, 'fiber': 2, 'category': 'fruits'},
}

def parse_food_text(text):
    """
    Parse food text input using NLP techniques
    Returns list of recognized foods with portions
    """
    text = text.lower().strip()
    foods_found = []
    
    # Extract portion information
    portion_patterns = {
        'oz': r'(\d+\.?\d*)\s*(?:oz|ounce|ounces)',
        'cup': r'(\d+\.?\d*|1/2|half)\s*(?:cup|cups)',
        'gram': r'(\d+\.?\d*)\s*(?:g|gram|grams)',
        'serving': r'(\d+\.?\d*)\s*(?:serving|servings)',
    }
    
    # Find all foods in the database that match
    for food_name, nutrition in FOOD_DATABASE.items():
        if food_name in text:
            portion = 1.0  # default serving
            portion_text = ""
            
            # Check for portion specifications
            if 'oz' in text or 'ounce' in text:
                match = re.search(portion_patterns['oz'], text)
                if match:
                    oz_amount = float(match.group(1))
                    portion = oz_amount / 4  # 4oz = 1 serving
                    portion_text = f"{oz_amount} oz"
            
            elif 'cup' in text:
                match = re.search(portion_patterns['cup'], text)
                if match:
                    cup_str = match.group(1)
                    if cup_str in ['1/2', 'half']:
                        portion = 0.5
                        portion_text = "1/2 cup"
                    else:
                        portion = float(cup_str)
                        portion_text = f"{portion} cup"
            
            elif 'gram' in text or ' g ' in text:
                match = re.search(portion_patterns['gram'], text)
                if match:
                    grams = float(match.group(1))
                    portion = grams / 100  # 100g = 1 serving
                    portion_text = f"{grams}g"
            
            # Calculate nutrition for this portion
            portioned_nutrition = {
                k: round(v * portion, 1) 
                for k, v in nutrition.items() 
                if k != 'category'
            }
            
            foods_found.append({
                'name': food_name.title(),
                'portion': portion,
                'portion_text': portion_text or f"{portion} serving",
                'nutrition': portioned_nutrition,
                'category': nutrition['category']
            })
    
    return foods_found

def analyze_eating_patterns(user_id):
    """Analyze user's eating patterns for recommendations"""
    logs = food_log_ops.get_recent_logs(user_id, days=14)
    
    if not logs:
        return None
    
    recent_logs = logs  # Already filtered to last 2 weeks
    
    patterns = {
        'total_meals': len(recent_logs),
        'avg_calories': 0,
        'avg_protein': 0,
        'food_frequency': defaultdict(int),
        'meal_times': defaultdict(int),
        'low_protein_days': 0,
        'high_calorie_days': 0,
    }
    
    daily_totals = defaultdict(lambda: {'calories': 0, 'protein': 0})
    
    for log in recent_logs:
        # Handle both string and datetime timestamps
        if isinstance(log['timestamp'], str):
            date = log['timestamp'].split('T')[0]
        else:
            date = log['timestamp'].date().isoformat()
        
        daily_totals[date]['calories'] += log['total_nutrition']['calories']
        daily_totals[date]['protein'] += log['total_nutrition']['protein']
        
        # Track food frequency
        for food in log['foods']:
            patterns['food_frequency'][food['name']] += 1
        
        # Track meal times
        hour = int(log['timestamp'].split('T')[1].split(':')[0])
        patterns['meal_times'][log['meal_type']] += 1
    
    # Calculate averages
    if daily_totals:
        patterns['avg_calories'] = sum(d['calories'] for d in daily_totals.values()) / len(daily_totals)
        patterns['avg_protein'] = sum(d['protein'] for d in daily_totals.values()) / len(daily_totals)
        
        for day_data in daily_totals.values():
            if day_data['protein'] < 80:
                patterns['low_protein_days'] += 1
            if day_data['calories'] > 2200:
                patterns['high_calorie_days'] += 1
    
    return patterns

def generate_recommendations(user_id):
    """Generate personalized recommendations based on patterns"""
    patterns = analyze_eating_patterns(user_id)
    recommendations = []
    
    if not patterns:
        recommendations.append({
            'type': 'welcome',
            'message': "Welcome! Start logging your meals to get personalized recommendations.",
            'icon': '👋'
        })
        return recommendations
    
    # Get today's logs
    today_logs = food_log_ops.get_today_logs(user_id)
    
    today_protein = sum(log['total_nutrition']['protein'] for log in today_logs)
    today_calories = sum(log['total_nutrition']['calories'] for log in today_logs)
    
    # Protein recommendation
    if today_protein < 60:
        recommendations.append({
            'type': 'protein',
            'message': f"You're at {round(today_protein)}g protein today (goal: 120g). Try adding grilled chicken, salmon, or Greek yogurt!",
            'icon': '💪'
        })
    
    # Calorie tracking
    if today_calories > 1800:
        recommendations.append({
            'type': 'calories',
            'message': f"You've consumed {round(today_calories)} calories today. Consider lighter options for your next meal.",
            'icon': '⚠️'
        })
    elif today_calories < 1200 and len(today_logs) >= 2:
        recommendations.append({
            'type': 'calories',
            'message': f"You're at {round(today_calories)} calories. Make sure you're eating enough to fuel your body!",
            'icon': '🍽️'
        })
    
    # Pattern-based recommendations
    if patterns['food_frequency']:
        most_common = max(patterns['food_frequency'].items(), key=lambda x: x[1])
        if most_common[1] >= 3:
            recommendations.append({
                'type': 'variety',
                'message': f"You've had {most_common[0]} {most_common[1]} times recently. Try mixing it up with similar healthy options!",
                'icon': '🔄'
            })
    
    # Positive reinforcement
    if today_protein >= 80 and today_calories <= 2000:
        recommendations.append({
            'type': 'positive',
            'message': "Excellent nutrition today! You're hitting your protein goals and staying within your calorie budget. Keep it up! 🎉",
            'icon': '✅'
        })
    
    # Default encouragement
    if not recommendations:
        recommendations.append({
            'type': 'positive',
            'message': "You're doing great! Keep logging your meals to track your progress.",
            'icon': '✨'
        })
    
    return recommendations


# Chat logging utilities
CHAT_LOG_DIR = os.path.join(os.path.dirname(__file__), 'chat_logs')
os.makedirs(CHAT_LOG_DIR, exist_ok=True)


def log_chat_interaction(user_id, message, result, status='success'):
    """Persist chat interactions (prompt + response) to JSON file and MongoDB."""
    try:
        timestamp = datetime.utcnow().isoformat()
        log_entry = {
            'user_id': user_id,
            'timestamp': timestamp,
            'status': status,
            'message': message,
            'agent_response': result.get('agent_response'),
            'foods': result.get('foods', []),
            'total_nutrition': result.get('total_nutrition', {}),
            'recommendations': result.get('recommendations', []),
            'intent': result.get('intent'),
            'needs_clarification': result.get('needs_clarification', False),
        }

        # Write JSON file per interaction
        safe_user = str(user_id).replace('@', '_at_').replace('.', '_')
        filename = f"chat_{safe_user}_{timestamp.replace(':', '-').replace('.', '-')}.json"
        filepath = os.path.join(CHAT_LOG_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(log_entry, f, ensure_ascii=False, indent=2)

        # Store in MongoDB (chat_logs collection)
        try:
            chat_collection = mongo_client.db['chat_logs']
            chat_collection.insert_one(log_entry)
        except Exception as e:
            print(f"⚠️ Failed to save chat log to MongoDB: {e}")
    except Exception as e:
        print(f"⚠️ Failed to log chat interaction: {e}")


# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return redirect(url_for('chat'))

@app.route('/chat')
def chat():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_ops.get_user_by_email(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('chat.html', user_name=user['name'])

@app.route('/calendar')
def calendar():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = user_ops.get_user_by_email(session['user_id'])
    if not user:
        session.clear()
        return redirect(url_for('login'))
    
    return render_template('calendar.html', user_name=user['name'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = user_ops.get_user_by_email(email)
        
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = email
            session.permanent = True
            return redirect(url_for('index'))
        
        return render_template('login.html', error='Invalid email or password')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        goals_json = request.form.get('goals')
        
        if user_ops.user_exists(email):
            if request.content_type == 'application/x-www-form-urlencoded':
                return render_template('register.html', error='Email already registered')
            return jsonify({'error': 'Email already registered'}), 400
        
        password_hash = generate_password_hash(password)
        
        # Parse custom goals if provided
        custom_goals = None
        if goals_json:
            try:
                custom_goals = json.loads(goals_json)
            except:
                pass
        
        result = user_ops.create_user(email, name, password_hash, custom_goals)
        
        if not result['success']:
            if request.content_type == 'application/x-www-form-urlencoded':
                return render_template('register.html', error='Registration failed. Please try again.')
            return jsonify({'error': 'Registration failed'}), 400
        
        session.clear()
        session['user_id'] = email
        session.permanent = True
        
        if request.content_type == 'application/x-www-form-urlencoded':
            return redirect(url_for('index'))
        return jsonify({'success': True}), 200
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/api/log-food', methods=['POST'])
def log_food():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    food_text = data.get('food_text', '')
    meal_type = data.get('meal_type', 'snack')
    
    if not food_text.strip():
        return jsonify({'error': 'Please enter food description'}), 400
    
    user_id = session['user_id']
    
    # Get user history for the agent
    user_history = food_log_ops.get_recent_logs(user_id, days=30)
    
    # Process food log using LangGraph Agent
    result = process_food_log(
        user_id=user_id,
        food_text=food_text,
        meal_type=meal_type,
        user_history=user_history
    )
    
    if not result['success']:
        return jsonify({
            'error': result.get('error', 'No food items recognized. Try being more specific.')
        }), 400
    
    # Create log entry in MongoDB
    log_entry = food_log_ops.create_log(
        user_id=user_id,
        meal_type=meal_type,
        foods=result['foods'],
        total_nutrition=result['total_nutrition'],
        original_text=food_text
    )
    
    return jsonify({
        'success': True,
        'foods': result['foods'],
        'total_nutrition': result['total_nutrition'],
        'recommendations': result.get('recommendations', []),
        'message': 'Meal logged successfully with AI analysis!'
    })

@app.route('/api/get-logs')
def get_logs():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    # Get today's logs from MongoDB
    today_logs = food_log_ops.get_today_logs(user_id)
    
    # Calculate daily totals
    daily_total = {
        'calories': sum(log['total_nutrition']['calories'] for log in today_logs),
        'protein': sum(log['total_nutrition']['protein'] for log in today_logs),
        'carbs': sum(log['total_nutrition']['carbs'] for log in today_logs),
        'fat': sum(log['total_nutrition']['fat'] for log in today_logs),
        'fiber': sum(log['total_nutrition']['fiber'] for log in today_logs),
    }
    
    # Get user goals
    user = user_ops.get_user_by_email(user_id)
    goals = user.get('goals', {
        'daily_calories': 2000,
        'daily_protein': 120,
        'daily_carbs': 250,
        'daily_fat': 65
    })
    
    return jsonify({
        'logs': today_logs,
        'daily_total': daily_total,
        'goals': goals
    })

@app.route('/api/get-recommendations')
def get_recommendations():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    recommendations = generate_recommendations(user_id)
    
    return jsonify({'recommendations': recommendations})

@app.route('/api/get-stats')
def get_stats():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    patterns = analyze_eating_patterns(user_id)
    
    if not patterns:
        return jsonify({'stats': None})
    
    stats = {
        'total_meals_logged': patterns['total_meals'],
        'avg_daily_calories': round(patterns['avg_calories']),
        'avg_daily_protein': round(patterns['avg_protein']),
        'most_common_foods': dict(sorted(
            patterns['food_frequency'].items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5])
    }
    
    return jsonify({'stats': stats})

@app.route('/api/chat-daily-suggestion')
def chat_daily_suggestion():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    
    today_logs = food_log_ops.get_today_logs(user_id)
    daily_total = {
        'calories': sum(log['total_nutrition']['calories'] for log in today_logs),
        'protein': sum(log['total_nutrition']['protein'] for log in today_logs),
        'carbs': sum(log['total_nutrition']['carbs'] for log in today_logs),
        'fat': sum(log['total_nutrition']['fat'] for log in today_logs),
        'fiber': sum(log['total_nutrition']['fiber'] for log in today_logs),
    }
    
    user = user_ops.get_user_by_email(user_id)
    goals = user.get('goals', {
        'daily_calories': 2000,
        'daily_protein': 120,
        'daily_carbs': 250,
        'daily_fat': 65
    })
    
    recommendations = generate_recommendations(user_id)
    
    if daily_total['calories'] == 0 and daily_total['protein'] == 0 and not today_logs:
        prefix = "Good day! It looks like you haven't logged anything yet today. "
    else:
        prefix = (
            f"So far today you're at {round(daily_total['calories'])} calories "
            f"and {round(daily_total['protein'])}g protein. "
        )
    
    tip = recommendations[0]['message'] if recommendations else (
        "Start by logging your first meal and I'll track your nutrition and give gentle suggestions."
    )
    
    agent_response = prefix + tip
    
    return jsonify({
        'success': True,
        'agent_response': agent_response,
        'recommendations': recommendations,
        'daily_total': daily_total,
        'goals': goals
    })

@app.route('/api/weekly-insight')
def weekly_insight():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    days = request.args.get('days', 7, type=int)
    
    logs = food_log_ops.get_recent_logs(user_id, days=days)
    
    if not logs:
        return jsonify({
            'summary': None,
            'insight': "Not enough data yet. Log meals for a couple of days and I'll summarize your week.",
            'suggestions': []
        })
    
    daily_totals = defaultdict(lambda: {
        'calories': 0,
        'protein': 0,
        'carbs': 0,
        'fat': 0
    })
    category_counts = defaultdict(int)
    
    for log in logs:
        if isinstance(log['timestamp'], str):
            date = log['timestamp'].split('T')[0]
        else:
            date = log['timestamp'].date().isoformat()
        
        totals = log['total_nutrition']
        daily_totals[date]['calories'] += totals.get('calories', 0)
        daily_totals[date]['protein'] += totals.get('protein', 0)
        daily_totals[date]['carbs'] += totals.get('carbs', 0)
        daily_totals[date]['fat'] += totals.get('fat', 0)
        
        for food in log.get('foods', []):
            category = food.get('category')
            if category:
                category_counts[category] += 1
    
    num_days = len(daily_totals)
    avg_calories = sum(v['calories'] for v in daily_totals.values()) / num_days
    avg_protein = sum(v['protein'] for v in daily_totals.values()) / num_days
    avg_carbs = sum(v['carbs'] for v in daily_totals.values()) / num_days
    
    fast_food_meals = category_counts.get('fast_food', 0) + category_counts.get('treats', 0)
    veg_meals = category_counts.get('vegetables', 0)
    fruit_meals = category_counts.get('fruits', 0)
    
    suggestions = []
    
    if fast_food_meals >= 2:
        suggestions.append("You've had fast food or treats several times. Try swapping one of those meals for a lighter home-cooked option this week.")
    if avg_carbs < 150:
        suggestions.append("Your average carbs are on the lower side. If you're active, consider adding more whole grains, fruits, or starchy vegetables.")
    if avg_protein < 70:
        suggestions.append("Protein looks a bit low on average. Add lean protein like chicken, fish, lentils, or Greek yogurt to your meals.")
    if avg_calories > 2200:
        suggestions.append("Overall calories are a bit high. Slightly smaller portions or cutting sugary drinks can make a big difference.")
    if veg_meals < num_days:
        suggestions.append("Most days could use more veggies. Aim to add at least one colorful vegetable to your main meals.")
    if fruit_meals < num_days:
        suggestions.append("You're not getting fruit every day. Add a piece of fruit as a snack or dessert to boost fiber and micronutrients.")
    
    if not suggestions:
        suggestions.append("Nice balance overall. Keep up the consistent logging and colorful, protein-balanced meals!")
    
    insight = (
        f"In the last {num_days} day{'s' if num_days != 1 else ''}, "
        f"you averaged about {round(avg_calories)} calories, "
        f"{round(avg_protein)}g protein, and {round(avg_carbs)}g carbs per day."
    )
    
    summary = {
        'days_considered': num_days,
        'avg_calories': round(avg_calories),
        'avg_protein': round(avg_protein),
        'avg_carbs': round(avg_carbs),
        'fast_food_meals': fast_food_meals,
        'vegetable_meals': veg_meals,
        'fruit_meals': fruit_meals
    }
    
    return jsonify({
        'summary': summary,
        'insight': insight,
        'suggestions': suggestions
    })

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """Conversational food logging endpoint"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    data = request.json
    message = data.get('message', '')
    conversation_history = data.get('conversation_history', [])
    
    if not message.strip():
        return jsonify({'error': 'Please enter a message'}), 400
    
    user_id = session['user_id']
    
    # Get user history for context
    user_history = food_log_ops.get_recent_logs(user_id, days=30)
    
    # Process message with conversational agent
    result = process_conversational_message(
        user_id=user_id,
        message=message,
        conversation_history=conversation_history,
        user_history=user_history
    )
    
    # If food was successfully logged, save to database
    if result.get('success') and result.get('foods'):
        # Determine meal type based on time
        hour = datetime.now().hour
        if hour < 11:
            meal_type = 'breakfast'
        elif hour < 15:
            meal_type = 'lunch'
        elif hour < 20:
            meal_type = 'dinner'
        else:
            meal_type = 'snack'
        
        # Create log entry
        log_entry = food_log_ops.create_log(
            user_id=user_id,
            meal_type=meal_type,
            foods=result['foods'],
            total_nutrition=result['total_nutrition'],
            original_text=message
        )
    
    # Persist chat interaction (prompt + response) to JSON file and MongoDB
    if result.get('success'):
        status = 'success'
    elif result.get('needs_clarification'):
        status = 'clarification'
    else:
        status = 'info'
    
    log_chat_interaction(user_id, message, result, status=status)

    return jsonify(result)

@app.route('/api/calendar-logs')
def calendar_logs():
    """Get logs organized by date for calendar view"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    user_id = session['user_id']
    days = request.args.get('days', 30, type=int)
    
    # Get logs for the specified period
    logs = food_log_ops.get_recent_logs(user_id, days=days)
    
    # Organize by date
    logs_by_date = defaultdict(lambda: {
        'meals': [],
        'total_calories': 0,
        'total_protein': 0,
        'total_carbs': 0,
        'total_fat': 0,
        'meal_count': 0
    })
    
    for log in logs:
        # Handle both string and datetime timestamps
        if isinstance(log['timestamp'], str):
            date = log['timestamp'].split('T')[0]
        else:
            date = log['timestamp'].date().isoformat()
        
        logs_by_date[date]['meals'].append(log)
        logs_by_date[date]['total_calories'] += log['total_nutrition']['calories']
        logs_by_date[date]['total_protein'] += log['total_nutrition']['protein']
        logs_by_date[date]['total_carbs'] += log['total_nutrition']['carbs']
        logs_by_date[date]['total_fat'] += log['total_nutrition']['fat']
        logs_by_date[date]['meal_count'] += 1
    
    # Convert to list and sort by date
    calendar_data = [
        {
            'date': date,
            'meals': data['meals'],
            'summary': {
                'total_calories': round(data['total_calories']),
                'total_protein': round(data['total_protein']),
                'total_carbs': round(data['total_carbs']),
                'total_fat': round(data['total_fat']),
                'meal_count': data['meal_count']
            }
        }
        for date, data in logs_by_date.items()
    ]
    
    calendar_data.sort(key=lambda x: x['date'], reverse=True)
    
    return jsonify({'calendar_data': calendar_data})

if __name__ == '__main__':
    print("=" * 60)
    print("🍽️  Mindful Eating Agent - Flask Backend")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
