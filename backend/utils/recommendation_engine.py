"""
Recommendation Engine
Generates personalized nutrition recommendations
"""

import random
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict

class RecommendationEngine:
    def __init__(self, thresholds: Dict, prompts: Dict):
        self.thresholds = thresholds
        self.prompts = prompts
    
    def analyze_patterns(self, user_history: List[Dict]) -> Dict[str, Any]:
        """Analyze eating patterns from user history"""
        if not user_history:
            return {'status': 'insufficient_data'}
        
        recent_logs = user_history[-14:]  # Last 2 weeks
        
        patterns = {
            'total_meals': len(recent_logs),
            'food_frequency': defaultdict(int),
            'avg_calories': 0,
            'avg_protein': 0,
            'low_protein_days': 0,
        }
        
        daily_totals = defaultdict(lambda: {'calories': 0, 'protein': 0})
        
        for log in recent_logs:
            date = log['timestamp'].split('T')[0]
            daily_totals[date]['calories'] += log['total_nutrition']['calories']
            daily_totals[date]['protein'] += log['total_nutrition']['protein']
            
            for food in log['foods']:
                patterns['food_frequency'][food['name']] += 1
        
        if daily_totals:
            patterns['avg_calories'] = sum(d['calories'] for d in daily_totals.values()) / len(daily_totals)
            patterns['avg_protein'] = sum(d['protein'] for d in daily_totals.values()) / len(daily_totals)
            
            for day_data in daily_totals.values():
                if day_data['protein'] < self.thresholds['low_protein']:
                    patterns['low_protein_days'] += 1
        
        return patterns
    
    def generate_recommendations(
        self, 
        nutrition_data: Dict, 
        user_history: List[Dict],
        patterns: Dict
    ) -> List[Dict[str, str]]:
        """Generate personalized recommendations"""
        recommendations = []
        
        # Get today's totals
        today = datetime.now().date().isoformat()
        today_logs = [log for log in user_history if log['timestamp'].startswith(today)]
        
        today_protein = sum(log['total_nutrition']['protein'] for log in today_logs)
        today_calories = sum(log['total_nutrition']['calories'] for log in today_logs)
        
        # Add current meal
        today_protein += nutrition_data.get('protein', 0)
        today_calories += nutrition_data.get('calories', 0)
        
        # Protein recommendations
        if today_protein < self.thresholds['low_protein']:
            recommendations.append({
                'type': 'protein',
                'message': f"Hey! You're at {round(today_protein)}g protein today. Your goal is {self.thresholds['target_protein']}g - try adding some chicken, fish, or Greek yogurt to your next meal! 💪",
                'icon': '💪'
            })
        elif today_protein >= self.thresholds['good_protein'] and today_protein < self.thresholds['target_protein']:
            recommendations.append({
                'type': 'protein',
                'message': f"Nice! You're at {round(today_protein)}g protein - almost at your {self.thresholds['target_protein']}g goal! Keep it up!",
                'icon': '🎯'
            })
        
        # Calorie recommendations
        if today_calories > self.thresholds['high_calories']:
            recommendations.append({
                'type': 'calories',
                'message': f"You're at {round(today_calories)} calories today. Maybe go for something lighter next time? You've got this! 😊",
                'icon': '⚠️'
            })
        elif today_calories < self.thresholds['low_calories'] and len(today_logs) >= 2:
            recommendations.append({
                'type': 'calories',
                'message': f"You're only at {round(today_calories)} calories. Make sure you're eating enough to fuel your body! 🍽️",
                'icon': '🍽️'
            })
        
        # Pattern-based recommendations
        if patterns.get('food_frequency'):
            most_common = max(patterns['food_frequency'].items(), key=lambda x: x[1])
            if most_common[1] >= self.thresholds['food_frequency_alert']:
                recommendations.append({
                    'type': 'variety',
                    'message': f"I noticed you've had {most_common[0]} {most_common[1]} times recently. Nothing wrong with that, but variety is the spice of life! Try something new? 🔄",
                    'icon': '🔄'
                })
        
        # Positive reinforcement
        if today_protein >= 100 and today_calories <= self.thresholds['target_calories']:
            recommendations.append({
                'type': 'positive',
                'message': "Wow! You're crushing it today! Perfect protein, great calorie balance. This is exactly what we're aiming for! 🎉🔥",
                'icon': '✅'
            })
        elif today_protein >= self.thresholds['good_protein'] and today_calories <= self.thresholds['target_calories'] + 100:
            recommendations.append({
                'type': 'positive',
                'message': "Looking good! You're hitting your nutrition goals today. Keep this momentum going! 💪",
                'icon': '✅'
            })
        
        # Consistency encouragement
        if len(today_logs) >= 3:
            recommendations.append({
                'type': 'positive',
                'message': "Love the consistency! You've logged 3+ meals today. That's how you build lasting habits! 🌟",
                'icon': '🌟'
            })
        
        # Default encouragement
        if not recommendations:
            encouragements = self.prompts.get('encouragements', [
                "Great job logging your meal! 😊"
            ])
            recommendations.append({
                'type': 'positive',
                'message': random.choice(encouragements),
                'icon': '✨'
            })
        
        return recommendations
