"""
Nutrition Cache System
Caches nutrition data in ChromaDB for fast lookups
"""

import json
import uuid
from typing import Dict, Optional
from datetime import datetime


class NutritionCache:
    """Cache nutrition data in ChromaDB"""
    
    def __init__(self, chroma_client):
        """Initialize nutrition cache"""
        self.client = chroma_client.client
        
        # Create or get nutrition cache collection
        self.collection = self.client.get_or_create_collection(
            name="nutrition_cache",
            metadata={"description": "Cached nutrition data from Gemini and static database"}
        )
        
        print("✅ Nutrition cache initialized")
    
    def set(self, food_name: str, nutrition_data: Dict):
        """
        Store nutrition data in cache
        
        Args:
            food_name: Name of the food
            nutrition_data: Nutrition information dict
        """
        try:
            # Normalize food name
            normalized_name = food_name.lower().strip()
            
            # Check if already exists
            existing = self.get(food_name)
            if existing:
                # Update existing entry
                results = self.collection.get(
                    where={"normalized_name": normalized_name}
                )
                if results['ids']:
                    self.collection.delete(ids=results['ids'])
            
            # Create cache entry
            cache_id = str(uuid.uuid4())
            
            cache_doc = {
                'normalized_name': normalized_name,
                'name': nutrition_data.get('name', food_name.title()),
                'calories': str(nutrition_data.get('calories', 0)),
                'protein': str(nutrition_data.get('protein', 0)),
                'carbs': str(nutrition_data.get('carbs', 0)),
                'fat': str(nutrition_data.get('fat', 0)),
                'fiber': str(nutrition_data.get('fiber', 0)),
                'category': nutrition_data.get('category', 'mixed'),
                'source': nutrition_data.get('source', 'manual'),
                'cached_at': datetime.now().isoformat()
            }
            
            # Store in ChromaDB
            self.collection.add(
                ids=[cache_id],
                documents=[normalized_name],
                metadatas=[cache_doc]
            )
            
            print(f"✅ Cached nutrition data for: {food_name}")
            
        except Exception as e:
            print(f"⚠️ Error caching nutrition data: {e}")
    
    def search_similar(self, food_name: str, limit: int = 5) -> list:
        """
        Search for similar foods in cache
        
        Args:
            food_name: Food name to search for
            limit: Maximum number of results
            
        Returns:
            List of similar food names
        """
        try:
            # Use ChromaDB's semantic search
            results = self.collection.query(
                query_texts=[food_name.lower()],
                n_results=limit
            )
            
            if results['ids'] and results['ids'][0]:
                similar_foods = []
                for metadata in results['metadatas'][0]:
                    similar_foods.append(metadata['name'])
                return similar_foods
            
            return []
            
        except Exception as e:
            print(f"⚠️ Error searching cache: {e}")
            return []
    
    def populate_from_static_db(self, food_database: Dict):
        """
        Populate cache with static food database (lazy loading - stores reference only)
        
        Args:
            food_database: Static food database dict
        """
        # Store reference to static database for lazy loading
        self.static_db = food_database
        print(f"✅ Nutrition cache ready with {len(food_database)} foods available")
    
    def get(self, food_name: str) -> Optional[Dict]:
        """
        Get nutrition data from cache (with lazy loading from static DB)
        
        Args:
            food_name: Name of the food (case-insensitive)
            
        Returns:
            Nutrition data dict or None if not found
        """
        try:
            # Normalize food name
            normalized_name = food_name.lower().strip()
            
            # First check static database (fast, no ChromaDB needed)
            if hasattr(self, 'static_db') and normalized_name in self.static_db:
                nutrition = self.static_db[normalized_name].copy()
                nutrition['name'] = normalized_name.title()
                nutrition['source'] = 'static'
                return nutrition
            
            # Then check ChromaDB cache for previously looked up items
            results = self.collection.get(
                where={"normalized_name": normalized_name}
            )
            
            if results['ids']:
                metadata = results['metadatas'][0]
                
                # Parse nutrition data
                nutrition = {
                    'name': metadata['name'],
                    'calories': float(metadata['calories']),
                    'protein': float(metadata['protein']),
                    'carbs': float(metadata['carbs']),
                    'fat': float(metadata['fat']),
                    'fiber': float(metadata['fiber']),
                    'category': metadata['category'],
                    'source': metadata.get('source', 'cache'),
                    'cached_at': metadata.get('cached_at', '')
                }
                
                return nutrition
            
            return None
            
        except Exception as e:
            print(f"⚠️ Error reading from nutrition cache: {e}")
            return None
