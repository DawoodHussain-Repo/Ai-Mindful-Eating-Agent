"""
Test MongoDB Integration
Quick test to verify all MongoDB operations work correctly
"""

from utils.mongodb_client import MongoDBClient, UserOperations, FoodLogOperations
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

def test_mongodb_integration():
    """Test all MongoDB operations"""
    
    print("=" * 60)
    print("Testing MongoDB Integration")
    print("=" * 60)
    
    try:
        # Initialize MongoDB
        print("\n[1/5] Connecting to MongoDB...")
        mongo_client = MongoDBClient('config/mongodb_config.json')
        user_ops = UserOperations(mongo_client)
        food_log_ops = FoodLogOperations(mongo_client)
        print("✅ Connected successfully")
        
        # Test user creation
        print("\n[2/5] Testing user creation...")
        test_email = f"test_{datetime.now().timestamp()}@example.com"
        password_hash = generate_password_hash("testpassword123")
        
        result = user_ops.create_user(
            email=test_email,
            name="Test User",
            password_hash=password_hash
        )
        
        if result['success']:
            print(f"✅ User created: {test_email}")
        else:
            print(f"❌ Failed to create user: {result.get('error')}")
            return False
        
        # Test user retrieval
        print("\n[3/5] Testing user retrieval...")
        user = user_ops.get_user_by_email(test_email)
        
        if user and user['email'] == test_email:
            print(f"✅ User retrieved: {user['name']}")
        else:
            print("❌ Failed to retrieve user")
            return False
        
        # Test food log creation
        print("\n[4/5] Testing food log creation...")
        log = food_log_ops.create_log(
            user_id=test_email,
            meal_type="breakfast",
            foods=[
                {
                    'name': 'Oatmeal',
                    'portion': 1.0,
                    'nutrition': {
                        'calories': 158,
                        'protein': 6,
                        'carbs': 27,
                        'fat': 3.2,
                        'fiber': 4
                    }
                }
            ],
            total_nutrition={
                'calories': 158,
                'protein': 6,
                'carbs': 27,
                'fat': 3.2,
                'fiber': 4
            },
            original_text="1 cup oatmeal"
        )
        
        if log:
            print(f"✅ Food log created: {log['meal_type']}")
        else:
            print("❌ Failed to create food log")
            return False
        
        # Test food log retrieval
        print("\n[5/5] Testing food log retrieval...")
        logs = food_log_ops.get_user_logs(test_email)
        
        if logs and len(logs) > 0:
            print(f"✅ Retrieved {len(logs)} food log(s)")
        else:
            print("❌ Failed to retrieve food logs")
            return False
        
        # Cleanup test data
        print("\n[Cleanup] Removing test data...")
        mongo_client.collections['users'].delete_one({'email': test_emai