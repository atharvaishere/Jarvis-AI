import chromadb
client = chromadb.PersistentClient(path="/Users/atharvashrivastava/Jarvis-AI/core/vector_db")
collection = client.get_or_create_collection(name="jarvis_conversations")
docs = collection.get()
print(f"Count: {collection.count()}")
for i, doc in enumerate(docs.get('documents', [])[:5]):
    print(f"Doc {i}: {doc}")
