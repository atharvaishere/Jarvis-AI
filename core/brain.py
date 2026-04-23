import json
import re
import os
from groq import Groq
from dotenv import load_dotenv
from core.memory import get_memory_string
from core.speak import speak_stream
from core.state import state
from core.rag_engine import search_knowledge

# Load environment variables from .env file
load_dotenv()

# Get Groq API key securely from .env
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please add it to your .env file.")

groq_client = Groq(api_key=GROQ_API_KEY)

def process_with_ai(user_input, chat_history):
    explicit_memories = get_memory_string()
    rag_context = search_knowledge(user_input)

    system_instruction = f"""
    You are Jarvis, a highly intelligent, natural-sounding AI assistant.
    CRITICAL: YOU MUST SPEAK COMPLETELY IN HINDI FROM NOW ON.
    Write your responses in natural Hindi (using Romanized/English script or Devanagari, but prefer fluent Hindi sentences).
    Keep your answers concise and friendly. Do not use repetitive crutch words.

    {explicit_memories}

    {rag_context}

    CRITICAL INSTRUCTION FOR MEMORIES & KNOWLEDGE BASE:
    Only use these facts to ANSWER direct questions about the user's past plans/preferences. DO NOT randomly bring up these facts in casual conversation just to show off that you know them!

    Analyze the user's input. The user can give MULTIPLE commands in one single sentence.
    You MUST output ONLY a valid JSON object containing a single key "commands" which is an ARRAY of objects.
    Each object in the array must have an "action", "target", and optionally "message" and "subject".

    Rules for "action":
    1. "open_app" -> For Mac apps ONLY. Target: Name of the app.
    2. "close_app" -> For closing or quitting a specific Mac app. Target: Name of the app.
    3. "play_youtube" -> CRITICAL: If the user says "play [something]". Target: The song/video name.
    4. "open_website" -> Target: "youtube.com", "google.com", etc.
    5. "wikipedia" -> Target: The search topic.
    6. "open_folder" -> Target: Folder name.
    7. "read_file" -> Target: File name.
    8. "get_time" -> Target: "time".
    9. "get_date" -> Target: "date".
    10. "get_battery" -> Target: "battery".
    11. "mac_control" -> Target MUST be EXACTLY one of: "volume_up", "volume_down", "volume_max", "volume_min", "mute", "brightness_up", "brightness_down", "play_pause", "focus_on", "focus_off", "minimize_window", "hide_all".
    12. "take_screenshot" -> Target: "screenshot".
    13. "get_weather" -> Target: "weather".
    14. "get_calendar" -> Event type or "all". NEVER use "calendar" as target.
    15. "hardware_control" -> Target MUST be EXACTLY one of: "wifi_on", "wifi_off", "sleep", "restart", "shutdown".
    16. "send_message" -> Target: Contact name. Message: text.
    17. "send_email" -> Target: Email address. Subject: subject. Message: body.
    18. "create_note" -> Target: The content of the note.
    19. "create_reminder" -> Target: The reminder text.
    20. "set_timer" -> Target: Duration strictly into SECONDS as a string.
    21. "run_shortcut" -> Target: Name of the shortcut.
    22. "save_memory" -> Target: The specific fact to save permanently.
    23. "exit_system" -> When user says goodbye, bye, stop, quit, or exit. Target: Your dynamic, natural 1-sentence Hindi farewell message.
    24. "chat" -> For general conversation, answering questions, telling jokes, or if input is unclear. Target: Your casual Hindi response.
    25. "read_screen" -> Target: "screen".
    26. "unsupported" -> When asked to read past Emails/Messages. Target: Your natural Hindi explanation that you cannot access those yet.

    EXAMPLES:
    Input: "volume full kardo, youtube open karo, aur ek timer lagao 5 minute ka"
    Output: {{"commands": [
        {{"action": "mac_control", "target": "volume_max"}},
        {{"action": "open_website", "target": "youtube.com"}},
        {{"action": "set_timer", "target": "300"}},
        {{"action": "chat", "target": "Sir, maine volume full kar diya hai, YouTube khol diya hai, aur 5 minute ka timer laga diya hai."}}
    ]}}

    Input: "goodbye jarvis"
    Output: {{"commands": [{{"action": "exit_system", "target": "Alvida sir. Aapka din shubh ho!"}}]}}

    Input: "SYSTEM: You have just been powered online. Give a VERY SHORT Hindi startup greeting (MAX 2-3 WORDS)."
    Output: {{"commands": [{{"action": "chat", "target": "Taiyaar hoon sir."}}]}}
    """

    messages = [{'role': 'system', 'content': system_instruction}]

    # Keep only the last 2 turns to keep input fast and clean
    recent_history = chat_history[-2:] if len(chat_history) > 2 else chat_history
    messages.extend(recent_history)

    messages.append({'role': 'user', 'content': user_input})

    print("⏳ Jarvis is thinking...", end="\r", flush=True)
    state.set_status("THINKING...")

    try:
        # Since Groq is lightning fast, we drop the complex streaming regex and just wait 0.2s for the full JSON array
        response = groq_client.chat.completions.create(
            model='llama-3.3-70b-versatile',
            messages=messages,
            response_format={"type": "json_object"},
            stream=False, # Disabled streaming for flawless Multi-Command Array parsing
            temperature=0.3,
            max_completion_tokens=400
        )

        full_json = response.choices[0].message.content
        data = json.loads(full_json)

        # Clear thinking text
        print(" " * 30, end="\r")

        return data.get('commands', [{"action": "chat", "target": "Maaf kijiye sir, main samajh nahi paya."}])

    except Exception as e:
        print(f"\n[Groq Error]: {e}")
        return [{"action": "chat", "target": "Sir, system mein kuch error hai ya internet connection toot gaya hai."}]
