"""
Quick script to check MongoDB connection and display database info
"""

from utils.mongodb_client import MongoDBClient, UserOperations, FoodLogOperations

def check_mongodb():
    """Check MongoDB connection and display info"""
    try:
        print("=" * 60)
        print("MongoDB Connection Check")
        print("=" * 60)
        
        # Initialize MongoDB
        mongo_client = MongoDBClient('config/mongodb_config.json')
        user_ops = UserOperations(mongo_client)
        food_log_ops = FoodLogOperations(mongo_client)
        
        # Get database stats
        db = mongo_client.db
        
        print(f"\n✅ Connected to database: {db.name}")
        print(f"\nCollections:")
        for collection_name in db.list_collection_names():
            count = db[collection_name].count_documents({})
            print(f"  - {collection_name}: {count} documents")
        
        print("\n" + "=" * 60)
        print("MongoDB is ready to use!")
        print("=" * 60)
        
        mongo_client.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease ensure:")
        print("1. MongoDB is installed")
        print("2. MongoDB service is running")
        print("3. MongoDB is accessible on localhost:27017")
        return False
    
    return True

if __name__ == '__main__':
    check_mongodb()
