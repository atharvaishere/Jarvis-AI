import sys
import time
import random
import subprocess
import threading

# Import Core Modules
from core.speak import speak, wait_for_speech
from core.listen import listen
from core.brain import process_with_ai

# Import Skill Modules
from skills.mac_ops import open_app, close_app, take_screenshot, mac_control, hardware_control
from skills.web_ops import open_website, play_youtube, search_wikipedia
from skills.daily_ops import get_time, get_date, get_battery, get_weather
from skills.calendar_ops import get_nearest_event
from skills.communications import send_imessage, send_email
from skills.file_ops import open_folder, read_file
from skills.productivity_ops import create_note, create_reminder, set_timer
from skills.shortcut_ops import run_apple_shortcut
from skills.screen_ops import summarize_screen
from core.memory import save_fact
from core.proactive import start_proactive_monitors
from core.state import state

# Global flag to control the main loop
JARVIS_ACTIVE = True

def chat_with_jarvis(run_as_thread=False):
    global JARVIS_ACTIVE
    JARVIS_ACTIVE = True

    # Start all background proactive monitoring threads
    start_proactive_monitors()

    print("\n🤖 Jarvis is booting up...\n")
    state.set_status("INITIALIZING...")

    chat_history = []
    is_awake = False

    # Ask the AI for a unique, dynamic startup greeting!
    commands = process_with_ai("SYSTEM: You have just been powered online. Give a VERY SHORT Hindi startup greeting (MAX 2-3 WORDS). For example: 'Taiyaar hoon sir', 'System chalu', or 'Namaste sir'.", chat_history)
    for cmd in commands:
        action = cmd.get('action', 'chat')
        target = cmd.get('target', '')
        chat_history.append({'role': 'assistant', 'content': target})
        if action == 'chat':
            speak(target)
            print(f"🗣️ Jarvis: {target}")

            wait_for_speech()

    print("\n💤 Jarvis is sleeping... (Say 'Jarvis' to wake me up)")
    state.set_status("SLEEPING...")

    while JARVIS_ACTIVE:
        try:
            if not is_awake:
                # Silently listen in the background for the wake word
                user_input = listen(quiet=True)

                if not user_input:
                    continue

                input_lower = user_input.lower()
                if 'jarvis' in input_lower:
                    is_awake = True
                    # Check if command was spoken together with the wake word (e.g. "Jarvis what is the time")
                    cleaned_input = input_lower.replace('hey jarvis', '').replace('hello jarvis', '').replace('jarvis', '').strip()

                    if cleaned_input == '':
                        # Only the wake word was spoken
                        subprocess.run(["afplay", "/System/Library/Sounds/Ping.aiff"])
                        print("\n🟢 Jarvis is awake and listening...")
                        continue
                    else:
                        # Wake word + command spoken together
                        user_input = cleaned_input
                else:
                    # Wake word not heard, stay asleep
                    continue
            else:
                # Jarvis is awake, listen actively for a command with a massive 240-second timeout (4 minutes)
                user_input = listen(quiet=False, active_timeout=240)

                if user_input == "TIMEOUT":
                    # User was completely silent for 4 minutes
                    is_awake = False
                    speak("Going back to sleep, sir.")
                    print("\n💤 Jarvis is sleeping... (Say 'Jarvis' to wake me up)")
                    continue
                elif user_input == "UNKNOWN" or not user_input:
                    # Heard random noise but no clear words. Ignore and stay awake.
                    continue

            print(f"You: {user_input}")
            state.add_log(f"You: {user_input}")

            # 1. Ask Llama to understand the intent
            commands = process_with_ai(user_input, chat_history)

            # 2. Execute based on the extracted intent
            for cmd in commands:
                action = cmd.get('action', 'chat')
                target = cmd.get('target', '')
                message = cmd.get('message', '')
                subject = cmd.get('subject', '')

                if action == 'exit_system':
                    chat_history.append({'role': 'assistant', 'content': target})
                    speak(target)
                    wait_for_speech()
                    if run_as_thread:
                        JARVIS_ACTIVE = False
                        print("\n💤 Jarvis thread stopped.")
                        return
                    else:
                        sys.exit(0)

                elif action == 'open_app':
                    open_app(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Opened {target}."})

                elif action == 'close_app':
                    close_app(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Closed {target}."})

                elif action == 'open_folder':
                    open_folder(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Opened {target} folder."})

                elif action == 'read_file':
                    read_file(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Attempted to read {target}."})

                elif action == 'play_youtube':
                    play_youtube(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Played {target} on YouTube."})

                elif action == 'open_website':
                    open_website(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Opened {target}."})

                elif action == 'wikipedia':
                    res = search_wikipedia(target, speak)
                    if res:
                        chat_history.append({'role': 'assistant', 'content': res})

                elif action == 'get_time':
                    res = get_time(speak)
                    chat_history.append({'role': 'assistant', 'content': f"Told the time: {res}"})

                elif action == 'get_date':
                    res = get_date(speak)
                    chat_history.append({'role': 'assistant', 'content': f"Told the date: {res}"})

                elif action == 'get_battery':
                    res = get_battery(speak)
                    if res:
                        chat_history.append({'role': 'assistant', 'content': f"Battery is at {res}."})

                elif action == 'get_weather':
                    res = get_weather(speak)
                    if res:
                        chat_history.append({'role': 'assistant', 'content': res})

                elif action == 'get_calendar':
                    res = get_nearest_event(target, speak)
                    chat_history.append({'role': 'assistant', 'content': res})

                elif action == 'create_note':
                    create_note(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Created note: {target}"})

                elif action == 'create_reminder':
                    create_reminder(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Created reminder: {target}"})

                elif action == 'set_timer':
                    set_timer(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Set timer for {target} seconds."})

                elif action == 'run_shortcut':
                    run_apple_shortcut(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Ran shortcut {target}."})

                elif action == 'save_memory':
                    save_fact(target)
                    speak("I've saved that to my permanent memory, sir.")
                    chat_history.append({'role': 'assistant', 'content': f"Saved fact: {target}"})

                elif action == 'take_screenshot':
                    take_screenshot(speak)
                    chat_history.append({'role': 'assistant', 'content': "Took a screenshot."})

                elif action == 'send_message':
                    send_imessage(target, message, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Sent message to {target}: {message}"})

                elif action == 'send_email':
                    send_email(target, subject, message, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Drafted email to {target}."})

                elif action == 'mac_control':
                    mac_control(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Performed Mac control: {target}"})

                elif action == 'hardware_control':
                    hardware_control(target, speak)
                    chat_history.append({'role': 'assistant', 'content': f"Performed hardware control: {target}"})

                elif action == 'read_screen':
                    summary = summarize_screen(speak, chat_history)
                    chat_history.append({'role': 'assistant', 'content': f"Screen summary: {summary}"})

                else:
                    # Fallback to general conversational chat
                    chat_history.append({'role': 'user', 'content': user_input})
                    chat_history.append({'role': 'assistant', 'content': target})
                    speak(target)
                    state.add_log(f"Jarvis: {target}")

            # Wait for all TTS audio to finish playing before starting to listen again
            wait_for_speech()

        except KeyboardInterrupt:
            if run_as_thread:
                JARVIS_ACTIVE = False
                break
            else:
                sys.exit(0)
        except Exception as e:
            print(f"\n[Error]: {e}")

if __name__ == "__main__":
    chat_with_jarvis()