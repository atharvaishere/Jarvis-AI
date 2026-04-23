import os
import glob
import chromadb
import uuid
try:
    from pypdf import PdfReader
except ImportError:
    pass

BRAIN_FOLDER = os.path.expanduser("~/Jarvis-AI/Jarvis-Brain")
DB_PATH = os.path.expanduser("~/Jarvis-AI/core/rag_db")

if not os.path.exists(BRAIN_FOLDER):
    os.makedirs(BRAIN_FOLDER)

def extract_text(file_path):
    """Extracts text from a single PDF or TXT file."""
    text = ""
    try:
        if file_path.lower().endswith('.pdf'):
            reader = PdfReader(file_path)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        elif file_path.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
    return text

def train_jarvis():
    """Reads all files in Jarvis-Brain and stores them as vectors in ChromaDB."""
    print(f"\n🧠 Scanning Jarvis-Brain folder: {BRAIN_FOLDER}")

    files = []
    for ext in ['*.pdf', '*.txt']:
        files.extend(glob.glob(os.path.join(BRAIN_FOLDER, ext)))

    if not files:
        print("No new documents found to learn from. Drop PDFs or Text files in the Jarvis-Brain folder!")
        return

    client = chromadb.PersistentClient(path=DB_PATH)
    collection = client.get_or_create_collection(name="knowledge_base")

    total_chunks_added = 0

    for file in files:
        file_name = os.path.basename(file)
        print(f"Reading and learning from: {file_name}...")

        # 1. Extract raw text
        full_text = extract_text(file)
        if not full_text.strip():
            continue

        # 2. Break the text into smaller chunks (e.g. 1000 characters each)
        chunk_size = 1000
        chunks = [full_text[i:i+chunk_size] for i in range(0, len(full_text), chunk_size)]

        # 3. Save chunks into Vector Database
        for i, chunk in enumerate(chunks):
            doc_id = f"{file_name}_chunk_{i}"

            # Check if this exact chunk was already learned (prevents duplicate data)
            existing = collection.get(ids=[doc_id])
            if not existing['ids']:
                collection.add(
                    documents=[chunk],
                    metadatas=[{"source": file_name}],
                    ids=[doc_id]
                )
                total_chunks_added += 1

    if total_chunks_added > 0:
        print(f"✅ Training complete! Jarvis learned {total_chunks_added} new pieces of information.")
    else:
        print(f"✅ I already know everything in the Jarvis-Brain folder, sir.")

def search_knowledge(query, n_results=2):
    """Searches the Vector Database for information relevant to the user's question."""
    try:
        client = chromadb.PersistentClient(path=DB_PATH)
        # Check if collection exists first
        try:
            collection = client.get_collection(name="knowledge_base")
        except:
            return "" # Collection doesn't exist yet

        if collection.count() == 0:
            return ""

        # Search the knowledge base for sentences similar to the query
        results = collection.query(query_texts=[query], n_results=n_results)

        if results['documents'] and results['documents'][0]:
            # Combine the top results into a single context string
            context = "\n---\n".join(results['documents'][0])
            return f"\n[JARVIS KNOWLEDGE BASE - USE THIS TO ANSWER THE QUESTION]:\n{context}\n"
        return ""
    except Exception as e:
        return ""

if __name__ == "__main__":
    train_jarvis()