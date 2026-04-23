import json
import os

# --- Explicit Fact Memory (memory.json) ---
MEMORY_FILE = os.path.expanduser("~/Jarvis-AI/core/memory.json")

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return []
    try:
        with open(MEMORY_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_fact(fact):
    memories = load_memory()
    memories.append(fact)
    with open(MEMORY_FILE, 'w') as f:
        json.dump(memories, f, indent=4)

def get_memory_string():
    memories = load_memory()
    if not memories:
        return ""
    return "Explicit Facts you must always remember:\n- " + "\n- ".join(memories)
