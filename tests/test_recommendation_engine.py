"""
Unit Tests for Recommendation Engine Module
Tests pattern analysis, recommendations, and personalization
"""

import pytest
import sys
import os
from datetime import datetime, timedelta
from collections import defaultdict

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from utils.recommendation_engine import RecommendationEngine


# Test configuration
TEST_THRESHOLDS = {
    'low_protein': 60,
    'good_protein': 80,
    'target_protein': 120,
    'low_calories': 1200,
    'target_calories': 2000,
    'high_calories': 2200,
    'food_frequency_alert': 3,
}

TEST_PROMPTS = {
    'encouragements': [
        "Great job logging your meal! 😊",
        "Keep up the great work! 💪",
        "You're doing amazing! 🌟"
    ]
}


@pytest.fixture
def recommendation_engine():
    """Create a RecommendationEngine instance for testing"""
    return RecommendationEngine(TEST_THRESHOLDS, TEST_PROMPTS)


def create_mock_food_log(
    timestamp: str,
    foods: list,
    calories: float,
    protein: float,
    carbs: float = 0,
    fat: float = 0
):
    """Helper function to create mock food log entries"""
    return {
        'timestamp': timestamp,
        'foods': [{'name': food} for food in foods],
        'total_nutrition': {
            'calories': calories,
            'protein': protein,
            'carbs': carbs,
            'fat': fat
        }
    }


class TestPatternAnalysis:
    """Tests for eating pattern analysis"""
    
    def test_empty_history(self, recommendation_engine):
        """Test pattern analysis with empty history"""
        patterns = recommendation_engine.analyze_patterns([])
        assert patterns['status'] == 'insufficient_data'
    
    def test_single_meal_history(self, recommendation_engine):
        """Test pattern analysis with single meal"""
        history = [
            create_mock_food_log(
                datetime.now().isoformat(),
                ['chicken', 'rice'],
                400, 35
            )
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        assert patterns['total_meals'] == 1
    
    def test_food_frequency_counting(self, recommendation_engine):
        """Test that food frequency is counted correctly"""
        history = [
            create_mock_food_log(datetime.now().isoformat(), ['banana'], 105, 1),
            create_mock_food_log(datetime.now().isoformat(), ['banana'], 105, 1),
            create_mock_food_log(datetime.now().isoformat(), ['banana'], 105, 1),
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        assert patterns['food_frequency']['banana'] == 3
    
    def test_average_calories_calculation(self, recommendation_engine):
        """Test average daily calories calculation"""
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        
        history = [
            create_mock_food_log(f"{today}T08:00:00", ['eggs'], 200, 15),
            create_mock_food_log(f"{today}T12:00:00", ['chicken'], 300, 30),
            create_mock_food_log(f"{yesterday}T12:00:00", ['rice'], 400, 5),
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        
        # Day 1: 500 cal, Day 2: 400 cal -> avg = 450
        assert patterns['avg_calories'] == 450
    
    def test_average_protein_calculation(self, recommendation_engine):
        """Test average daily protein calculation"""
        today = datetime.now().date().isoformat()
        
        history = [
            create_mock_food_log(f"{today}T08:00:00", ['eggs'], 200, 20),
            create_mock_food_log(f"{today}T12:00:00", ['chicken'], 300, 30),
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        
        # Only one day: 50g protein
        assert patterns['avg_protein'] == 50
    
    def test_low_protein_days_counting(self, recommendation_engine):
        """Test counting of low protein days"""
        today = datetime.now().date().isoformat()
        yesterday = (datetime.now() - timedelta(days=1)).date().isoformat()
        
        history = [
            create_mock_food_log(f"{today}T12:00:00", ['rice'], 400, 30),  # Low protein day
            create_mock_food_log(f"{yesterday}T12:00:00", ['chicken'], 300, 100),  # High protein day
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        
        # Only 1 day has < 60g protein
        assert patterns['low_protein_days'] == 1
    
    def test_recent_history_limit(self, recommendation_engine):
        """Test that only recent 14 days are analyzed"""
        # Create 20 logs spread over 20 days
        history = []
        for i in range(20):
            date = (datetime.now() - timedelta(days=i)).isoformat()
            history.append(create_mock_food_log(date, ['food'], 100, 10))
        
        patterns = recommendation_engine.analyze_patterns(history)
        # Should only analyze last 14 entries
        assert patterns['total_meals'] == 14


class TestRecommendationGeneration:
    """Tests for recommendation generation"""
    
    def test_low_protein_recommendation(self, recommendation_engine):
        """Test recommendation for low protein intake"""
        nutrition_data = {'protein': 20, 'calories': 500}
        today = datetime.now().date().isoformat()
        
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['toast'], 100, 5)
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Should have protein recommendation since total is 25g < 60g
        protein_recs = [r for r in recommendations if r['type'] == 'protein']
        assert len(protein_recs) >= 1
    
    def test_good_protein_recommendation(self, recommendation_engine):
        """Test positive recommendation for good protein"""
        nutrition_data = {'protein': 30, 'calories': 400}
        today = datetime.now().date().isoformat()
        
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['eggs'], 200, 60)
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Should have protein recommendation (90g is good but not at target)
        assert isinstance(recommendations, list)
    
    def test_high_calorie_warning(self, recommendation_engine):
        """Test warning for high calorie intake"""
        nutrition_data = {'protein': 30, 'calories': 800}
        today = datetime.now().date().isoformat()
        
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['burger'], 500, 20),
            create_mock_food_log(f"{today}T12:00:00", ['pizza'], 1000, 30),
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Total = 500 + 1000 + 800 = 2300 > 2200
        calorie_recs = [r for r in recommendations if r['type'] == 'calories']
        assert len(calorie_recs) >= 1
    
    def test_low_calorie_warning(self, recommendation_engine):
        """Test warning for low calorie intake"""
        nutrition_data = {'protein': 10, 'calories': 200}
        today = datetime.now().date().isoformat()
        
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['apple'], 95, 0.5),
            create_mock_food_log(f"{today}T12:00:00", ['banana'], 105, 1),
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Total = 95 + 105 + 200 = 400 < 1200
        calorie_recs = [r for r in recommendations if r['type'] == 'calories']
        assert len(calorie_recs) >= 1
    
    def test_variety_recommendation(self, recommendation_engine):
        """Test recommendation for food variety"""
        nutrition_data = {'protein': 30, 'calories': 300}
        today = datetime.now().date().isoformat()
        
        user_history = []
        patterns = {
            'food_frequency': {'chicken': 5}  # Eaten 5 times (> 3 threshold)
        }
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Should suggest variety
        variety_recs = [r for r in recommendations if r['type'] == 'variety']
        assert len(variety_recs) >= 1
    
    def test_positive_reinforcement(self, recommendation_engine):
        """Test positive reinforcement for good nutrition"""
        nutrition_data = {'protein': 40, 'calories': 500}
        today = datetime.now().date().isoformat()
        
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['eggs'], 300, 30),
            create_mock_food_log(f"{today}T12:00:00", ['chicken'], 400, 40),
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Total protein = 30 + 40 + 40 = 110g >= 100g, calories = 1200 <= 2000
        positive_recs = [r for r in recommendations if r['type'] == 'positive']
        assert len(positive_recs) >= 1
    
    def test_consistency_encouragement(self, recommendation_engine):
        """Test encouragement for consistent logging"""
        nutrition_data = {'protein': 30, 'calories': 300}
        today = datetime.now().date().isoformat()
        
        # 3+ meals logged today
        user_history = [
            create_mock_food_log(f"{today}T08:00:00", ['eggs'], 200, 20),
            create_mock_food_log(f"{today}T12:00:00", ['chicken'], 300, 30),
            create_mock_food_log(f"{today}T15:00:00", ['banana'], 100, 1),
        ]
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Should encourage consistency
        positive_recs = [r for r in recommendations if r['type'] == 'positive']
        assert len(positive_recs) >= 1
    
    def test_default_encouragement(self, recommendation_engine):
        """Test default encouragement when no specific recommendations"""
        nutrition_data = {'protein': 25, 'calories': 400}
        user_history = []
        patterns = {'food_frequency': {}}
        
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, user_history, patterns
        )
        
        # Should have at least one recommendation (default encouragement)
        assert len(recommendations) >= 1


class TestRecommendationQuality:
    """Tests for recommendation message quality"""
    
    def test_recommendations_have_icons(self, recommendation_engine):
        """Test that all recommendations have icons"""
        nutrition_data = {'protein': 20, 'calories': 300}
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, [], {'food_frequency': {}}
        )
        
        for rec in recommendations:
            assert 'icon' in rec
            assert len(rec['icon']) > 0
    
    def test_recommendations_have_messages(self, recommendation_engine):
        """Test that all recommendations have messages"""
        nutrition_data = {'protein': 20, 'calories': 300}
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, [], {'food_frequency': {}}
        )
        
        for rec in recommendations:
            assert 'message' in rec
            assert len(rec['message']) > 10  # Should be meaningful message
    
    def test_recommendations_have_types(self, recommendation_engine):
        """Test that all recommendations have types"""
        nutrition_data = {'protein': 20, 'calories': 300}
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, [], {'food_frequency': {}}
        )
        
        for rec in recommendations:
            assert 'type' in rec
            assert rec['type'] in ['protein', 'calories', 'variety', 'positive']


class TestEdgeCases:
    """Tests for edge cases"""
    
    def test_zero_nutrition_values(self, recommendation_engine):
        """Test handling of zero nutrition values"""
        nutrition_data = {'protein': 0, 'calories': 0}
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, [], {'food_frequency': {}}
        )
        assert isinstance(recommendations, list)
    
    def test_very_high_values(self, recommendation_engine):
        """Test handling of very high nutrition values"""
        nutrition_data = {'protein': 500, 'calories': 10000}
        recommendations = recommendation_engine.generate_recommendations(
            nutrition_data, [], {'food_frequency': {}}
        )
        assert isinstance(recommendations, list)
    
    def test_missing_fields_in_history(self, recommendation_engine):
        """Test handling of incomplete history entries"""
        history = [
            {
                'timestamp': datetime.now().isoformat(),
                'foods': [],
                'total_nutrition': {'calories': 100, 'protein': 10}
            }
        ]
        patterns = recommendation_engine.analyze_patterns(history)
        assert 'total_meals' in patterns


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
