"""Test local ChromaDB"""
import warnings
warnings.filterwarnings('ignore')

print("Testing local ChromaDB...")

try:
    print("1. Importing chromadb...")
    import chromadb
    print("   ✅ Success")
    
    print("\n2. Creating persistent client...")
    client = chromadb.PersistentClient(path="./chroma_data")
    print("   ✅ Success")
    
    print("\n3. Creating test collection...")
    collection = client.get_or_create_collection("test")
    print("   ✅ Success")
    
    print("\n4. Adding test data...")
    collection.add(
        ids=["test1"],
        documents=["test document"],
        metadatas=[{"test": "data"}]
    )
    print("   ✅ Success")
    
    print("\n5. Querying data...")
    results = collection.get(ids=["test1"])
    print(f"   ✅ Success: {results['ids']}")
    
    print("\n✅ All tests passed! Local ChromaDB works!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
