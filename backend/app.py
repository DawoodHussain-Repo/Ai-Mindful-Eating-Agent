"""
Mindful Eating Agent - Flask Backend
Text-based food logging with AI-powered nutrition analysis using LangGraph
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from datetime import datetime, timedelta
import json
import os
from werkzeug.security import generate_password_hash, check_password_hash
from collections import defaultdict
import re

# Import LangGraph Agent
from agent import process_food_log, mindful_eating_agent

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# In-memory storage (replace with database in production)
users_db = {}
food_logs_db = {}
user_patterns_db = {}

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
    if user_id not in food_logs_db or not food_logs_db[user_id]:
        return None
    
    logs = food_logs_db[user_id]
    recent_logs = logs[-14:]  # Last 2 weeks
    
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
        date = log['timestamp'].split('T')[0]
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
    today = datetime.now().date().isoformat()
    today_logs = [log for log in food_logs_db.get(user_id, []) 
                  if log['timestamp'].startswith(today)]
    
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

# Routes
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', user_name=users_db[session['user_id']]['name'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if email in users_db and check_password_hash(users_db[email]['password'], password):
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
        
        if email in users_db:
            return render_template('register.html', error='Email already registered')
        
        users_db[email] = {
            'name': name,
            'password': generate_password_hash(password),
            'created_at': datetime.now().isoformat(),
            'goals': {
                'daily_calories': 2000,
                'daily_protein': 120,
                'daily_carbs': 250,
                'daily_fat': 65
            }
        }
        food_logs_db[email] = []
        user_patterns_db[email] = {}
        
        session['user_id'] = email
        session.permanent = True
        return redirect(url_for('index'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
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
    user_history = food_logs_db.get(user_id, [])
    
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
    
    # Create log entry
    log_entry = {
        'id': len(food_logs_db.get(user_id, [])) + 1,
        'timestamp': datetime.now().isoformat(),
        'meal_type': meal_type,
        'foods': result['foods'],
        'total_nutrition': result['total_nutrition'],
        'original_text': food_text
    }
    
    if user_id not in food_logs_db:
        food_logs_db[user_id] = []
    food_logs_db[user_id].append(log_entry)
    
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
    logs = food_logs_db.get(user_id, [])
    
    # Get today's logs
    today = datetime.now().date().isoformat()
    today_logs = [log for log in logs if log['timestamp'].startswith(today)]
    
    # Calculate daily totals
    daily_total = {
        'calories': sum(log['total_nutrition']['calories'] for log in today_logs),
        'protein': sum(log['total_nutrition']['protein'] for log in today_logs),
        'carbs': sum(log['total_nutrition']['carbs'] for log in today_logs),
        'fat': sum(log['total_nutrition']['fat'] for log in today_logs),
        'fiber': sum(log['total_nutrition']['fiber'] for log in today_logs),
    }
    
    # Get user goals
    goals = users_db[user_id].get('goals', {
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

if __name__ == '__main__':
    print("=" * 60)
    print("🍽️  Mindful Eating Agent - Flask Backend")
    print("=" * 60)
    print("Server starting on http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("=" * 60)
    app.run(debug=True, host='0.0.0.0', port=5000)
