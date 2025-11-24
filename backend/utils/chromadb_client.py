"""
ChromaDB Client Utility
Handles all ChromaDB connections and operations for Mindful Eating App
"""

import chromadb
from chromadb.config import Settings
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import json
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ChromaDBClient:
    """ChromaDB client for Mindful Eating App"""
    
    def __init__(self):
        """Initialize ChromaDB client with configuration from .env"""
        self.api_key = os.getenv('CHROMA_API_KEY')
        self.tenant = os.getenv('CHROMA_TENANT')
        self.database = os.getenv('CHROMA_DATABASE')
        
        # Try cloud first, fallback to local
        use_local = os.getenv('CHROMA_USE_LOCAL', 'false').lower() == 'true'
        
        if use_local or not all([self.api_key, self.tenant, self.database]):
            # Use local persistent storage
            print("⚠️ Using local ChromaDB storage (Python 3.13 compatible)")
            self.client = chromadb.PersistentClient(path="./chroma_data")
            self.database = "local"
        else:
            # Use cloud ChromaDB
            try:
                self.client = chromadb.HttpClient(
                    host="api.trychroma.com",
                    port=443,
                    ssl=True,
                    headers={"x-chroma-token": self.api_key},
                    tenant=self.tenant,
                    database=self.database
                )
            except Exception as e:
                print(f"⚠️ Cloud ChromaDB failed: {e}")
                print("⚠️ Falling back to local storage")
                self.client = chromadb.PersistentClient(path="./chroma_data")
                self.database = "local"
        
        # Initialize collections
        self.users_collection = None
        self.food_logs_collection = None
        self.sessions_collection = None
        self.chat_logs_collection = None
        
        self._initialize_collections()
        
        print(f"✅ Connected to ChromaDB: {self.database}")
    
    def _initialize_collections(self):
        """Create or get collections"""
        try:
            # Users collection
            self.users_collection = self.client.get_or_create_collection(
                name="users",
                metadata={"description": "User accounts and profiles"}
            )
            
            # Food logs collection
            self.food_logs_collection = self.client.get_or_create_collection(
                name="food_logs",
                metadata={"description": "User food logging history"}
            )
            
            # Sessions collection
            self.sessions_collection = self.client.get_or_create_collection(
                name="sessions",
                metadata={"description": "User session management"}
            )
            
            # Chat logs collection
            self.chat_logs_collection = self.client.get_or_create_collection(
                name="chat_logs",
                metadata={"description": "Chat interaction logs"}
            )
            
        except Exception as e:
            print(f"❌ Error initializing collections: {e}")
            raise
    
    def get_collection(self, collection_name: str):
        """Get a collection by name"""
        collections = {
            'users': self.users_collection,
            'food_logs': self.food_logs_collection,
            'sessions': self.sessions_collection,
            'chat_logs': self.chat_logs_collection
        }
        return collections.get(collection_name)


class UserOperations:
    """Handle all user-related database operations"""
    
    def __init__(self, chroma_client: ChromaDBClient):
        self.collection = chroma_client.users_collection
    
    def create_user(self, email: str, name: str, password_hash: str, custom_goals: Optional[Dict] = None) -> Dict:
        """Create a new user"""
        default_goals = {
            'daily_calories': 2000,
            'daily_protein': 120,
            'daily_carbs': 250,
            'daily_fat': 65
        }
        
        goals = custom_goals if custom_goals else default_goals
        
        # Check if user already exists
        if self.user_exists(email):
            return {'success': False, 'error': 'User already exists'}
        
        user_id = str(uuid.uuid4())
        user_doc = {
            'email': email,
            'name': name,
            'password': password_hash,
            'created_at': datetime.now().isoformat(),
            'goals': json.dumps(goals)  # Serialize goals to JSON string
        }
        
        try:
            self.collection.add(
                ids=[user_id],
                documents=[email],  # Use email as document for searchability
                metadatas=[user_doc]
            )
            return {'success': True, 'user_id': user_id}
        except Exception as e:
            print(f"❌ Error creating user: {e}")
            import traceback
            traceback.print_exc()
            return {'success': False, 'error': str(e)}
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            results = self.collection.get(
                where={"email": email}
            )
            
            if results['ids']:
                user_data = results['metadatas'][0].copy()
                user_data['_id'] = results['ids'][0]
                # Parse goals from JSON string
                if 'goals' in user_data and isinstance(user_data['goals'], str):
                    user_data['goals'] = json.loads(user_data['goals'])
                return user_data
            return None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
    
    def update_user_goals(self, email: str, goals: Dict) -> bool:
        """Update user's nutrition goals"""
        try:
            user = self.get_user_by_email(email)
            if not user:
                return False
            
            # Prepare metadata without _id
            user_metadata = {k: v for k, v in user.items() if k != '_id'}
            user_metadata['goals'] = json.dumps(goals)
            
            self.collection.update(
                ids=[user['_id']],
                metadatas=[user_metadata]
            )
            return True
        except Exception as e:
            print(f"Error updating goals: {e}")
            return False
    
    def user_exists(self, email: str) -> bool:
        """Check if user exists"""
        try:
            results = self.collection.get(
                where={"email": email}
            )
            return len(results['ids']) > 0
        except:
            return False


class FoodLogOperations:
    """Handle all food log database operations"""
    
    def __init__(self, chroma_client: ChromaDBClient):
        self.collection = chroma_client.food_logs_collection
    
    def create_log(self, user_id: str, meal_type: str, foods: List[Dict], 
                   total_nutrition: Dict, original_text: str) -> Dict:
        """Create a new food log entry"""
        log_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        log_doc = {
            'user_id': user_id,
            'timestamp': timestamp.isoformat(),
            'meal_type': meal_type,
            'foods': json.dumps(foods),  # Store as JSON string
            'total_nutrition': json.dumps(total_nutrition),
            'original_text': original_text
        }
        
        # Create searchable document from food names
        food_names = ', '.join([f['name'] for f in foods])
        document = f"{meal_type}: {food_names} - {original_text}"
        
        try:
            self.collection.add(
                ids=[log_id],
                documents=[document],
                metadatas=[log_doc]
            )
            
            # Return formatted log
            return {
                '_id': log_id,
                'user_id': user_id,
                'timestamp': timestamp.isoformat(),
                'meal_type': meal_type,
                'foods': foods,
                'total_nutrition': total_nutrition,
                'original_text': original_text
            }
        except Exception as e:
            print(f"Error creating log: {e}")
            return {}
    
    def get_user_logs(self, user_id: str, limit: Optional[int] = None, 
                     start_date: Optional[datetime] = None, 
                     end_date: Optional[datetime] = None) -> List[Dict]:
        """Get user's food logs with optional filters"""
        try:
            # Build where clause
            where_clause = {"user_id": user_id}
            
            # Get all logs for user
            results = self.collection.get(
                where=where_clause
            )
            
            if not results['ids']:
                return []
            
            # Parse and filter logs
            logs = []
            for i, log_id in enumerate(results['ids']):
                metadata = results['metadatas'][i]
                
                # Parse timestamp
                log_timestamp = datetime.fromisoformat(metadata['timestamp'])
                
                # Apply date filters
                if start_date and log_timestamp < start_date:
                    continue
                if end_date and log_timestamp > end_date:
                    continue
                
                # Parse JSON fields
                log = {
                    '_id': log_id,
                    'user_id': metadata['user_id'],
                    'timestamp': metadata['timestamp'],
                    'meal_type': metadata['meal_type'],
                    'foods': json.loads(metadata['foods']),
                    'total_nutrition': json.loads(metadata['total_nutrition']),
                    'original_text': metadata['original_text']
                }
                logs.append(log)
            
            # Sort by timestamp (newest first)
            logs.sort(key=lambda x: x['timestamp'], reverse=True)
            
            # Apply limit
            if limit:
                logs = logs[:limit]
            
            return logs
            
        except Exception as e:
            print(f"Error getting logs: {e}")
            return []
    
    def get_today_logs(self, user_id: str) -> List[Dict]:
        """Get today's logs for a user"""
        today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return self.get_user_logs(user_id, start_date=today_start, end_date=today_end)
    
    def get_recent_logs(self, user_id: str, days: int = 14) -> List[Dict]:
        """Get recent logs for pattern analysis"""
        start_date = datetime.now() - timedelta(days=days)
        return self.get_user_logs(user_id, start_date=start_date)
    
    def delete_log(self, log_id: str, user_id: str) -> bool:
        """Delete a food log entry"""
        try:
            # Verify ownership
            results = self.collection.get(ids=[log_id])
            if not results['ids']:
                return False
            
            metadata = results['metadatas'][0]
            if metadata['user_id'] != user_id:
                return False
            
            self.collection.delete(ids=[log_id])
            return True
        except Exception as e:
            print(f"Error deleting log: {e}")
            return False


class SessionOperations:
    """Handle session management in ChromaDB"""
    
    def __init__(self, chroma_client: ChromaDBClient):
        self.collection = chroma_client.sessions_collection
    
    def create_session(self, session_id: str, user_id: str, expiry: datetime):
        """Create a new session"""
        session_doc = {
            'id': session_id,
            'user_id': user_id,
            'created_at': datetime.now().isoformat(),
            'expiration': expiry.isoformat()
        }
        
        try:
            self.collection.add(
                ids=[session_id],
                documents=[user_id],
                metadatas=[session_doc]
            )
        except Exception as e:
            print(f"Error creating session: {e}")
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session by ID"""
        try:
            results = self.collection.get(ids=[session_id])
            if results['ids']:
                return results['metadatas'][0]
            return None
        except:
            return None
    
    def delete_session(self, session_id: str):
        """Delete a session"""
        try:
            self.collection.delete(ids=[session_id])
        except Exception as e:
            print(f"Error deleting session: {e}")
    
    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions"""
        try:
            # Get all sessions
            results = self.collection.get()
            
            if not results['ids']:
                return 0
            
            now = datetime.now()
            expired_ids = []
            
            for i, session_id in enumerate(results['ids']):
                metadata = results['metadatas'][i]
                expiry = datetime.fromisoformat(metadata['expiration'])
                
                if expiry < now:
                    expired_ids.append(session_id)
            
            if expired_ids:
                self.collection.delete(ids=expired_ids)
            
            return len(expired_ids)
        except Exception as e:
            print(f"Error cleaning up sessions: {e}")
            return 0


class ChatLogOperations:
    """Handle chat log operations"""
    
    def __init__(self, chroma_client: ChromaDBClient):
        self.collection = chroma_client.chat_logs_collection
    
    def create_chat_log(self, user_id: str, message: str, result: Dict, status: str = 'success'):
        """Create a chat log entry"""
        log_id = str(uuid.uuid4())
        timestamp = datetime.now()
        
        log_doc = {
            'user_id': user_id,
            'timestamp': timestamp.isoformat(),
            'status': status,
            'message': message,
            'agent_response': result.get('agent_response', ''),
            'foods': json.dumps(result.get('foods', [])),
            'total_nutrition': json.dumps(result.get('total_nutrition', {})),
            'recommendations': json.dumps(result.get('recommendations', [])),
            'intent': result.get('intent', ''),
            'needs_clarification': str(result.get('needs_clarification', False))
        }
        
        try:
            self.collection.add(
                ids=[log_id],
                documents=[f"{user_id}: {message}"],
                metadatas=[log_doc]
            )
        except Exception as e:
            print(f"Error creating chat log: {e}")
