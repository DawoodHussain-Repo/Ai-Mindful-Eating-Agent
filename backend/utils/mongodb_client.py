"""
MongoDB Client Utility
Handles all MongoDB connections and operations
"""

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import json
import os
from datetime import datetime

class MongoDBClient:
    """MongoDB client for Mindful Eating App"""
    
    def __init__(self, config_path='config/mongodb_config.json'):
        """Initialize MongoDB client with configuration"""
        self.config = self._load_config(config_path)
        self.client = None
        self.db = None
        self.collections = {}
        self._connect()
    
    def _load_config(self, config_path):
        """Load MongoDB configuration from JSON file"""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Default configuration
            return {
                "connection": {
                    "host": "localhost",
                    "port": 27017,
                    "database": "mindful_eating_db"
                },
                "collections": {
                    "users": "users",
                    "food_logs": "food_logs",
                    "sessions": "sessions"
                }
            }
    
    def _connect(self):
        """Establish connection to MongoDB"""
        try:
            conn_config = self.config['connection']
            connection_string = f"mongodb://{conn_config['host']}:{conn_config['port']}/"
            
            self.client = MongoClient(
                connection_string,
                serverSelectionTimeoutMS=5000
            )
            
            # Test connection
            self.client.admin.command('ping')
            
            # Get database
            self.db = self.client[conn_config['database']]
            
            # Initialize collections
            for key, collection_name in self.config['collections'].items():
                self.collections[key] = self.db[collection_name]
            
            # Create indexes
            self._create_indexes()
            
            print(f"✅ Connected to MongoDB: {conn_config['database']}")
            
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"❌ MongoDB Connection Error: {e}")
            print("Make sure MongoDB is running on localhost:27017")
            raise
    
    def _create_indexes(self):
        """Create necessary indexes for better performance"""
        # User email index (unique)
        self.collections['users'].create_index('email', unique=True)
        
        # Food logs indexes
        self.collections['food_logs'].create_index('user_id')
        self.collections['food_logs'].create_index('timestamp')
        self.collections['food_logs'].create_index([('user_id', 1), ('timestamp', -1)])
        
        # Session index
        self.collections['sessions'].create_index('session_id', unique=True)
        self.collections['sessions'].create_index('expiry')
    
    def get_collection(self, collection_name):
        """Get a collection by name"""
        return self.collections.get(collection_name)
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

# User Operations
class UserOperations:
    """Handle all user-related database operations"""
    
    def __init__(self, mongo_client):
        self.users = mongo_client.get_collection('users')
    
    def create_user(self, email, name, password_hash, custom_goals=None):
        """Create a new user"""
        default_goals = {
            'daily_calories': 2000,
            'daily_protein': 120,
            'daily_carbs': 250,
            'daily_fat': 65
        }
        
        # Use custom goals if provided, otherwise use defaults
        goals = custom_goals if custom_goals else default_goals
        
        user_doc = {
            'email': email,
            'name': name,
            'password': password_hash,
            'created_at': datetime.now(),
            'goals': goals
        }
        
        try:
            result = self.users.insert_one(user_doc)
            return {'success': True, 'user_id': str(result.inserted_id)}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_user_by_email(self, email):
        """Get user by email"""
        return self.users.find_one({'email': email})
    
    def update_user_goals(self, email, goals):
        """Update user's nutrition goals"""
        result = self.users.update_one(
            {'email': email},
            {'$set': {'goals': goals}}
        )
        return result.modified_count > 0
    
    def user_exists(self, email):
        """Check if user exists"""
        return self.users.count_documents({'email': email}) > 0

# Food Log Operations
class FoodLogOperations:
    """Handle all food log database operations"""
    
    def __init__(self, mongo_client):
        self.food_logs = mongo_client.get_collection('food_logs')
    
    def create_log(self, user_id, meal_type, foods, total_nutrition, original_text):
        """Create a new food log entry"""
        log_doc = {
            'user_id': user_id,
            'timestamp': datetime.now(),
            'meal_type': meal_type,
            'foods': foods,
            'total_nutrition': total_nutrition,
            'original_text': original_text
        }
        
        result = self.food_logs.insert_one(log_doc)
        log_doc['_id'] = str(result.inserted_id)
        return log_doc
    
    def get_user_logs(self, user_id, limit=None, start_date=None, end_date=None):
        """Get user's food logs with optional filters"""
        query = {'user_id': user_id}
        
        if start_date or end_date:
            query['timestamp'] = {}
            if start_date:
                query['timestamp']['$gte'] = start_date
            if end_date:
                query['timestamp']['$lte'] = end_date
        
        cursor = self.food_logs.find(query).sort('timestamp', -1)
        
        if limit:
            cursor = cursor.limit(limit)
        
        logs = []
        for log in cursor:
            log['_id'] = str(log['_id'])
            log['timestamp'] = log['timestamp'].isoformat()
            logs.append(log)
        
        return logs
    
    def get_today_logs(self, user_id):
        """Get today's logs for a user"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.get_user_logs(user_id, start_date=today_start, end_date=today_end)
    
    def get_recent_logs(self, user_id, days=14):
        """Get recent logs for pattern analysis"""
        from datetime import timedelta
        start_date = datetime.now() - timedelta(days=days)
        
        return self.get_user_logs(user_id, start_date=start_date)
    
    def delete_log(self, log_id, user_id):
        """Delete a food log entry"""
        from bson.objectid import ObjectId
        result = self.food_logs.delete_one({
            '_id': ObjectId(log_id),
            'user_id': user_id
        })
        return result.deleted_count > 0

# Session Operations
class SessionOperations:
    """Handle session management in MongoDB"""
    
    def __init__(self, mongo_client):
        self.sessions = mongo_client.get_collection('sessions')
    
    def create_session(self, session_id, user_id, expiry):
        """Create a new session"""
        session_doc = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.now(),
            'expiry': expiry
        }
        
        self.sessions.insert_one(session_doc)
    
    def get_session(self, session_id):
        """Get session by ID"""
        return self.sessions.find_one({'session_id': session_id})
    
    def delete_session(self, session_id):
        """Delete a session"""
        self.sessions.delete_one({'session_id': session_id})
    
    def cleanup_expired_sessions(self):
        """Remove expired sessions"""
        result = self.sessions.delete_many({
            'expiry': {'$lt': datetime.now()}
        })
        return result.deleted_count
