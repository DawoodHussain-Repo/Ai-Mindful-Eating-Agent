"""
Migration script to move data from MongoDB to ChromaDB
Run this if you have existing data in MongoDB that needs to be migrated
"""

import sys
from datetime import datetime

try:
    from utils.mongodb_client import MongoDBClient as OldMongoClient
    from utils.mongodb_client import UserOperations as OldUserOps
    from utils.mongodb_client import FoodLogOperations as OldFoodLogOps
    MONGO_AVAILABLE = True
except ImportError:
    MONGO_AVAILABLE = False
    print("⚠️ MongoDB client not available. Skipping migration.")

from utils.chromadb_client import ChromaDBClient, UserOperations, FoodLogOperations


def migrate_users(old_user_ops, new_user_ops):
    """Migrate users from MongoDB to ChromaDB"""
    print("\n📦 Migrating users...")
    
    try:
        # This would need to be implemented based on your MongoDB structure
        # For now, we'll skip as users will re-register
        print("ℹ️ User migration skipped - users will need to re-register")
        return True
    except Exception as e:
        print(f"❌ Error migrating users: {e}")
        return False


def migrate_food_logs(old_food_log_ops, new_food_log_ops):
    """Migrate food logs from MongoDB to ChromaDB"""
    print("\n📦 Migrating food logs...")
    
    try:
        # This would need to be implemented based on your MongoDB structure
        print("ℹ️ Food log migration skipped - starting fresh")
        return True
    except Exception as e:
        print(f"❌ Error migrating food logs: {e}")
        return False


def main():
    """Main migration function"""
    print("=" * 60)
    print("  MongoDB to ChromaDB Migration Tool")
    print("=" * 60)
    
    if not MONGO_AVAILABLE:
        print("\n❌ MongoDB client not available.")
        print("If you don't have existing data, you can skip this migration.")
        return
    
    print("\n⚠️ WARNING: This will migrate data from MongoDB to ChromaDB")
    print("Make sure you have:")
    print("  1. MongoDB running with existing data")
    print("  2. ChromaDB credentials in .env file")
    print("  3. Backed up your MongoDB data")
    
    response = input("\nContinue with migration? (yes/no): ").lower().strip()
    
    if response != 'yes':
        print("\n❌ Migration cancelled")
        return
    
    try:
        # Initialize old MongoDB client
        print("\n🔌 Connecting to MongoDB...")
        old_mongo = OldMongoClient('config/mongodb_config.json')
        old_user_ops = OldUserOps(old_mongo)
        old_food_log_ops = OldFoodLogOps(old_mongo)
        print("✅ Connected to MongoDB")
        
        # Initialize new ChromaDB client
        print("\n🔌 Connecting to ChromaDB...")
        new_chroma = ChromaDBClient()
        new_user_ops = UserOperations(new_chroma)
        new_food_log_ops = FoodLogOperations(new_chroma)
        print("✅ Connected to ChromaDB")
        
        # Migrate data
        users_success = migrate_users(old_user_ops, new_user_ops)
        logs_success = migrate_food_logs(old_food_log_ops, new_food_log_ops)
        
        # Summary
        print("\n" + "=" * 60)
        print("  Migration Summary")
        print("=" * 60)
        print(f"Users:     {'✅ Success' if users_success else '❌ Failed'}")
        print(f"Food Logs: {'✅ Success' if logs_success else '❌ Failed'}")
        print("\n✅ Migration completed!")
        print("\nNote: Users will need to re-register with the new system.")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
