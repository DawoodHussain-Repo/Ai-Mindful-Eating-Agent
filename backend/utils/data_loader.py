"""
Data Loader Utility
Loads and parses JSON configuration files
"""

import json
import os
from typing import Dict, Any

def load_json(file_path: str) -> Dict[str, Any]:
    """Load JSON file and return parsed data"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Warning: {file_path} not found. Using empty dict.")
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing {file_path}: {e}")
        return {}

def get_data_path(filename: str) -> str:
    """Get absolute path to data file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    return os.path.join(backend_dir, 'data', filename)

def get_config_path(filename: str) -> str:
    """Get absolute path to config file"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.dirname(current_dir)
    return os.path.join(backend_dir, 'config', filename)

# Load all data files
def load_food_database() -> Dict[str, Any]:
    """Load complete food database"""
    return load_json(get_data_path('food_database.json'))

def load_user_prompts() -> Dict[str, str]:
    """Load user-friendly prompts"""
    return load_json(get_config_path('prompts.json'))

def load_app_config() -> Dict[str, Any]:
    """Load application configuration"""
    return load_json(get_config_path('app_config.json'))

def load_nutrition_goals() -> Dict[str, Any]:
    """Load default nutrition goals"""
    return load_json(get_config_path('nutrition_goals.json'))
