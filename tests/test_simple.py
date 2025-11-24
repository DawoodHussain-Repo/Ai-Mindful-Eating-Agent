"""Simple test"""
import warnings
import sys
warnings.filterwarnings('ignore')

print("Testing ChromaDB connection...")
print("Python version:", sys.version)
print()

try:
    print("1. Loading environment...")
    from dotenv import load_dotenv
    import os
    load_dotenv()
    print(f"   CHROMA_API_KEY: {'✅ Found' if os.getenv('CHROMA_API_KEY') else '❌ Missing'}")
    print(f"   CHROMA_TENANT: {'✅ Found' if os.getenv('CHROMA_TENANT') else '❌ Missing'}")
    print(f"   CHROMA_DATABASE: {'✅ Found' if os.getenv('CHROMA_DATABASE') else '❌ Missing'}")
    print()
    
    print("2. Importing chromadb...")
    import chromadb
    print("   ✅ chromadb imported")
    print()
    
    print("3. Creating HTTP client...")
    client = chromadb.HttpClient(
        host="api.trychroma.com",
        port=443,
        ssl=True,
        headers={"x-chroma-token": os.getenv('CHROMA_API_KEY')},
        tenant=os.getenv('CHROMA_TENANT'),
        database=os.getenv('CHROMA_DATABASE')
    )
    print("   ✅ HTTP client created")
    print()
    
    print("4. Testing heartbeat...")
    client.heartbeat()
    print("   ✅ Heartbeat successful!")
    print()
    
    print("✅ All tests passed!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
