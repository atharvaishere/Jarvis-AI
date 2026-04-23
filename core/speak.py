import subprocess
import re
import threading
import queue
import asyncio
import edge_tts
import tempfile
import os
from core.state import state

# Create a queue for Zero-Latency Streaming TTS
tts_queue = queue.Queue()

async def generate_and_play(text):
    """Generates hyper-realistic TTS via Microsoft Edge Neural API and plays it."""
    # Use proper Hindi Male Neural Voice for authentic Hindi speaking
    voice = "hi-IN-MadhurNeural"
    try:
        # Generate the audio file (very fast over internet)
        # Increased rate to +40% for faster delivery
        communicate = edge_tts.Communicate(text, voice, rate="+40%")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        await communicate.save(temp_path)

        # Play using Mac's native afplay command
        subprocess.run(["afplay", temp_path])

        # Cleanup
        os.remove(temp_path)
    except Exception as e:
        print(f"Neural TTS Error: {e}. Falling back to default Mac Voice.")
        # If offline or API fails, instantly fallback to old Mac voice (using Lekha for Hindi fallback)
        subprocess.run(['say', '-v', 'Lekha', '-r', '260', text])

def tts_worker():
    while True:
        text = tts_queue.get()
        if text is None:
            break
        clean_text = clean_text_for_speech(text)
        if clean_text.strip():
            state.set_status("SPEAKING...")
            state.add_log(f"Jarvis: {clean_text}")

            # Use the new async Neural Voice function
            asyncio.run(generate_and_play(clean_text))

            state.set_status("SLEEPING...")
        tts_queue.task_done()

# Start the background worker thread for streaming TTS
threading.Thread(target=tts_worker, daemon=True).start()

def clean_text_for_speech(text):
    text = re.sub(r'[*_#~]', '', text)
    text = text.replace('"', '').replace("'", "")
    return text

def speak(text):
    """Synchronous speaking for standard skill outputs."""
    clean_text = clean_text_for_speech(text)
    state.set_status("SPEAKING...")
    state.add_log(f"Jarvis: {clean_text}")

    # Use the new async Neural Voice function
    asyncio.run(generate_and_play(clean_text))

    state.set_status("SLEEPING...")

def speak_stream(sentence):
    """Asynchronous speaking for Zero-Latency LLM streaming."""
    tts_queue.put(sentence)

def wait_for_speech():
    """Wait until the TTS queue is empty (finished speaking)."""
    tts_queue.join()
