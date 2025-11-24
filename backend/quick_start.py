"""
Quick Start - Minimal test to verify the app can run
"""

print("=" * 60)
print("  AI Mindful Eating Agent - Quick Start")
print("=" * 60)
print()

# Test basic imports
print("Testing imports...")
try:
    from flask import Flask
    print("✅ Flask")
except:
    print("❌ Flask - run: pip install Flask")
    exit(1)

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv")
except:
    print("❌ python-dotenv - run: pip install python-dotenv")
    exit(1)

try:
    import chromadb
    print("✅ ChromaDB")
except:
    print("❌ ChromaDB - run: pip install chromadb")
    exit(1)

try:
    import google.generativeai as genai
    print("✅ Google Generative AI")
except:
    print("❌ Google Generative AI - run: pip install langchain-google-genai")
    exit(1)

print()
print("=" * 60)
print("  All core dependencies installed!")
print("=" * 60)
print()
print("Starting Flask application...")
print()

# Start the app
import app
