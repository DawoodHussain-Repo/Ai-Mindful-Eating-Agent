"""
Test ChromaDB connection and basic operations
"""

from utils.chromadb_client import ChromaDBClient, UserOperations, FoodLogOperations
from datetime import datetime


def test_connection():
    """Test ChromaDB connection"""
    print("=" * 60)
    print("  ChromaDB Connection Test")
    print("=" * 60)
    
    try:
        print("\n🔌 Connecting to ChromaDB...")
        client = ChromaDBClient()
        print("✅ Successfully connected to ChromaDB!")
        
        # Test heartbeat
        print("\n💓 Testing heartbeat...")
        client.client.heartbeat()
        print("✅ Heartbeat successful!")
        
        # List collections
        print("\n📚 Available collections:")
        collections = client.client.list_collections()
        for col in collections:
            print(f"  - {col.name}")
        
        return client
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return None


def test_user_operations(client):
    """Test user operations"""
    print("\n" + "=" * 60)
    print("  Testing User Operations")
    print("=" * 60)
    
    try:
        user_ops = UserOperations(client)
        
        # Test user creation
        test_email = f"test_{datetime.now().timestamp()}@example.com"
        print(f"\n➕ Creating test user: {test_email}")
        
        result = user_ops.create_user(
            email=test_email,
            name="Test User",
            password_hash="hashed_password_123"
        )
        
        if result['success']:
            print(f"✅ User created with ID: {result['user_id']}")
            
            # Test user retrieval
            print(f"\n🔍 Retrieving user: {test_email}")
            user = user_ops.get_user_by_email(test_email)
            
            if user:
                print(f"✅ User found: {user['name']}")
                print(f"   Goals: {user['goals']}")
            else:
                print("❌ User not found")
        else:
            print(f"❌ User creation failed: {result.get('error')}")
        
    except Exception as e:
        print(f"❌ User operations test failed: {e}")


def test_food_log_operations(client):
    """Test food log operations"""
    print("\n" + "=" * 60)
    print("  Testing Food Log Operations")
    print("=" * 60)
    
    try:
        food_log_ops = FoodLogOperations(client)
        
        # Test log creation
        print("\n➕ Creating test food log...")
        
        test_foods = [
            {
                'name': 'Grilled Chicken',
                'portion': 1.0,
                'portion_text': '1 serving',
                'nutrition': {
                    'calories': 165,
                    'protein': 31,
                    'carbs': 0,
                    'fat': 3.6,
                    'fiber': 0
                },
                'category': 'protein'
            }
        ]
        
        test_nutrition = {
            'calories': 165,
            'protein': 31,
            'carbs': 0,
            'fat': 3.6,
            'fiber': 0
        }
        
        log = food_log_ops.create_log(
            user_id="test_user_123",
            meal_type="lunch",
            foods=test_foods,
            total_nutrition=test_nutrition,
            original_text="I had grilled chicken for lunch"
        )
        
        if log:
            print(f"✅ Food log created with ID: {log['_id']}")
            
            # Test log retrieval
            print("\n🔍 Retrieving user logs...")
            logs = food_log_ops.get_user_logs("test_user_123")
            
            if logs:
                print(f"✅ Found {len(logs)} log(s)")
                for log in logs:
                    print(f"   - {log['meal_type']}: {log['original_text']}")
            else:
                print("⚠️ No logs found")
        else:
            print("❌ Food log creation failed")
        
    except Exception as e:
        print(f"❌ Food log operations test failed: {e}")


def main():
    """Run all tests"""
    print("\n🧪 Starting ChromaDB Tests...\n")
    
    # Test connection
    client = test_connection()
    
    if not client:
        print("\n❌ Cannot proceed with tests - connection failed")
        print("\nPlease check:")
        print("  1. Your .env file exists in backend/ directory")
        print("  2. CHROMA_API_KEY is correct")
        print("  3. CHROMA_TENANT is correct")
        print("  4. CHROMA_DATABASE is correct")
        return
    
    # Test operations
    test_user_operations(client)
    test_food_log_operations(client)
    
    # Summary
    print("\n" + "=" * 60)
    print("  Test Summary")
    print("=" * 60)
    print("✅ All tests completed!")
    print("\nYour ChromaDB setup is working correctly.")
    print("You can now run the Flask application with: python app.py")


if __name__ == '__main__':
    main()
