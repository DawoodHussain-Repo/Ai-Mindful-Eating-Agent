"""
Test if all required modules can be imported
"""

import sys

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"❌ {package_name or module_name}: {e}")
        return False

print("=" * 60)
print("  Testing Module Imports")
print("=" * 60)
print()

# Core dependencies
print("Core Dependencies:")
test_import("flask", "Flask")
test_import("werkzeug", "Werkzeug")
test_import("dotenv", "python-dotenv")
print()

# AI/ML dependencies
print("AI/ML Dependencies:")
test_import("langgraph", "LangGraph")
test_import("langchain", "LangChain")
test_import("langchain_core", "LangChain Core")
test_import("langchain_google_genai", "LangChain Google GenAI")
test_import("google.generativeai", "Google Generative AI")
print()

# Database
print("Database:")
test_import("chromadb", "ChromaDB")
print()

# Other
print("Other Dependencies:")
test_import("sentence_transformers", "Sentence Transformers")
test_import("cachetools", "CacheTools")
print()

print("=" * 60)
print("  Import Test Complete")
print("=" * 60)
