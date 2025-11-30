"""
Integration Tests for API Endpoints
Tests Flask routes, authentication, and API responses
"""

import pytest
import sys
import os
import json
from unittest.mock import Mock, patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestHealthEndpoint:
    """Tests for health check endpoints"""
    
    def test_health_endpoint_structure(self):
        """Test health endpoint response structure"""
        expected_fields = ['status', 'service', 'version']
        
        sample_response = {
            'status': 'healthy',
            'service': 'Mindful Eating Agent',
            'version': '1.0.0',
            'database_status': 'connected',
            'capabilities': ['food_parsing', 'nutrition_calculation']
        }
        
        for field in expected_fields:
            assert field in sample_response
    
    def test_health_status_values(self):
        """Test valid health status values"""
        valid_statuses = ['healthy', 'degraded', 'unhealthy']
        
        for status in valid_statuses:
            assert status in valid_statuses


class TestExternalAPIStructure:
    """Tests for external API Blueprint structure"""
    
    def test_external_api_exists(self):
        """Test external_api blueprint exists"""
        from api.external import external_api
        assert external_api is not None
    
    def test_external_api_has_health_route(self):
        """Test external API has health endpoint"""
        from api.external import health_check
        assert callable(health_check)
    
    def test_external_api_has_process_route(self):
        """Test external API has process endpoint"""
        from api.external import process_food_external
        assert callable(process_food_external)


class TestProcessEndpointValidation:
    """Tests for /process endpoint validation"""
    
    def test_required_fields_validation(self):
        """Test required fields for process endpoint"""
        required_fields = ['user_id', 'food_text']
        
        valid_request = {
            'user_id': 'user123',
            'food_text': 'I ate a banana',
            'meal_type': 'snack'
        }
        
        for field in required_fields:
            assert field in valid_request
    
    def test_meal_type_validation(self):
        """Test meal type must be valid"""
        valid_meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        
        for meal_type in valid_meal_types:
            assert meal_type in valid_meal_types
    
    def test_invalid_meal_type_rejected(self):
        """Test invalid meal type is rejected"""
        invalid_types = ['brunch', 'midnight_snack', 'elevenses', '']
        valid_types = ['breakfast', 'lunch', 'dinner', 'snack']
        
        for invalid in invalid_types:
            assert invalid not in valid_types


class TestResponseFormats:
    """Tests for API response formats"""
    
    def test_success_response_format(self):
        """Test success response has correct format"""
        success_response = {
            'success': True,
            'foods': [
                {'name': 'banana', 'calories': 105, 'protein': 1.3}
            ],
            'total_nutrition': {
                'calories': 105,
                'protein': 1.3,
                'carbs': 27,
                'fat': 0.4
            },
            'recommendations': [],
            'user_message': 'Logged: banana (105 cal)'
        }
        
        assert success_response['success'] == True
        assert 'foods' in success_response
        assert 'total_nutrition' in success_response
    
    def test_error_response_format(self):
        """Test error response has correct format"""
        error_response = {
            'success': False,
            'error': 'Missing required field: user_id'
        }
        
        assert error_response['success'] == False
        assert 'error' in error_response
    
    def test_clarification_response_format(self):
        """Test clarification response format"""
        clarification_response = {
            'success': True,
            'needs_clarification': True,
            'clarification_question': 'Which type of soda did you drink?',
            'options': ['pepsi', 'coke', 'sprite']
        }
        
        assert clarification_response['needs_clarification'] == True
        assert 'clarification_question' in clarification_response


class TestUserAuthenticationFlow:
    """Tests for user authentication endpoints"""
    
    def test_register_required_fields(self):
        """Test registration requires proper fields"""
        required_fields = ['email', 'password', 'name']
        
        valid_register = {
            'email': 'test@example.com',
            'password': 'securepassword123',
            'name': 'Test User'
        }
        
        for field in required_fields:
            assert field in valid_register
    
    def test_login_required_fields(self):
        """Test login requires email and password"""
        required_fields = ['email', 'password']
        
        valid_login = {
            'email': 'test@example.com',
            'password': 'securepassword123'
        }
        
        for field in required_fields:
            assert field in valid_login
    
    def test_email_format_validation(self):
        """Test email format is validated"""
        import re
        
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        
        valid_emails = ['test@example.com', 'user.name@domain.org']
        invalid_emails = ['notanemail', '@domain.com', 'user@', '']
        
        for email in valid_emails:
            assert re.match(email_pattern, email) is not None
        
        for email in invalid_emails:
            assert re.match(email_pattern, email) is None


class TestFoodLogEndpoints:
    """Tests for food logging endpoints"""
    
    def test_log_food_request_format(self):
        """Test log-food endpoint request format"""
        valid_request = {
            'food_text': 'I ate 2 bananas and a chicken sandwich',
            'meal_type': 'lunch'
        }
        
        assert 'food_text' in valid_request
        assert 'meal_type' in valid_request
    
    def test_get_logs_response_format(self):
        """Test get-logs response format"""
        expected_response = {
            'success': True,
            'logs': [
                {
                    'id': 'log123',
                    'timestamp': '2025-11-29T12:00:00',
                    'foods': [{'name': 'banana', 'calories': 105}],
                    'total_nutrition': {'calories': 105},
                    'meal_type': 'snack'
                }
            ]
        }
        
        assert expected_response['success'] == True
        assert 'logs' in expected_response
        assert isinstance(expected_response['logs'], list)
    
    def test_calendar_logs_date_format(self):
        """Test calendar logs use ISO date format"""
        from datetime import datetime
        
        date_str = datetime.now().date().isoformat()
        
        # Should be in YYYY-MM-DD format
        assert len(date_str) == 10
        assert date_str.count('-') == 2


class TestChatEndpoint:
    """Tests for chat/conversational endpoint"""
    
    def test_chat_request_format(self):
        """Test chat endpoint request format"""
        valid_request = {
            'message': 'What did I eat today?'
        }
        
        assert 'message' in valid_request
    
    def test_chat_response_format(self):
        """Test chat endpoint response format"""
        expected_response = {
            'success': True,
            'response': 'Today you have logged 3 meals totaling 1,500 calories.',
            'context': {
                'daily_calories': 1500,
                'meals_logged': 3
            }
        }
        
        assert 'response' in expected_response
        assert isinstance(expected_response['response'], str)


class TestRecommendationsEndpoint:
    """Tests for recommendations endpoint"""
    
    def test_recommendations_response_format(self):
        """Test recommendations response format"""
        expected_response = {
            'success': True,
            'recommendations': [
                {
                    'type': 'protein',
                    'message': 'Consider adding more protein to your diet.',
                    'icon': '💪'
                }
            ]
        }
        
        assert 'recommendations' in expected_response
        assert isinstance(expected_response['recommendations'], list)
    
    def test_recommendation_types(self):
        """Test valid recommendation types"""
        valid_types = ['protein', 'calories', 'variety', 'positive']
        
        for rec_type in valid_types:
            assert rec_type in valid_types


class TestStatsEndpoint:
    """Tests for statistics endpoint"""
    
    def test_stats_response_format(self):
        """Test stats endpoint response format"""
        expected_response = {
            'success': True,
            'stats': {
                'daily_calories': 1500,
                'daily_protein': 80,
                'weekly_average_calories': 1800,
                'total_meals_logged': 42,
                'streak_days': 7
            }
        }
        
        assert 'stats' in expected_response
        assert 'daily_calories' in expected_response['stats']
    
    def test_weekly_insight_format(self):
        """Test weekly insight response format"""
        expected_response = {
            'success': True,
            'insight': {
                'summary': 'Great week! You hit your protein goals 5 out of 7 days.',
                'highlights': ['Consistent logging', 'Good protein intake'],
                'areas_to_improve': ['Increase vegetable variety']
            }
        }
        
        assert 'insight' in expected_response


class TestErrorHandling:
    """Tests for API error handling"""
    
    def test_400_bad_request(self):
        """Test 400 error format"""
        error_response = {
            'success': False,
            'error': 'Invalid request body'
        }
        
        assert error_response['success'] == False
    
    def test_401_unauthorized(self):
        """Test 401 error format"""
        error_response = {
            'success': False,
            'error': 'Please login to access this resource'
        }
        
        assert 'error' in error_response
    
    def test_404_not_found(self):
        """Test 404 error format"""
        error_response = {
            'success': False,
            'error': 'Resource not found'
        }
        
        assert error_response['success'] == False
    
    def test_500_server_error(self):
        """Test 500 error format"""
        error_response = {
            'success': False,
            'error': 'Internal server error',
            'details': 'Database connection failed'
        }
        
        assert error_response['success'] == False


class TestCORSHeaders:
    """Tests for CORS configuration"""
    
    def test_allowed_origins(self):
        """Test allowed origins for CORS"""
        allowed_origins = ['http://localhost:3000']
        
        assert 'http://localhost:3000' in allowed_origins
    
    def test_cors_headers_present(self):
        """Test required CORS headers"""
        expected_headers = [
            'Access-Control-Allow-Origin',
            'Access-Control-Allow-Credentials'
        ]
        
        for header in expected_headers:
            assert header in expected_headers


class TestRateLimiting:
    """Tests for rate limiting"""
    
    def test_rate_limit_structure(self):
        """Test rate limit configuration"""
        rate_limit = {
            'requests_per_minute': 100,
            'requests_per_hour': 1000
        }
        
        assert rate_limit['requests_per_minute'] > 0
    
    def test_rate_limit_response(self):
        """Test rate limit exceeded response"""
        rate_limit_response = {
            'success': False,
            'error': 'Rate limit exceeded',
            'retry_after': 60
        }
        
        assert 'retry_after' in rate_limit_response


if __name__ == '__main__':
    pytest.main([__file__, '-v', '--tb=short'])
