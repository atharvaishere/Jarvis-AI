import os
import subprocess
import threading

def create_note(content, speak_func):
    speak_func("Creating a new note for you, sir.")

    # AppleScript to create a note natively on macOS
    applescript = f'''
    tell application "Notes"
        activate
        tell account "On My Mac"
            make new note at folder "Notes" with properties {{body:"{content}"}}
        end tell
    end tell
    '''
    # If "On My Mac" doesn't work (iCloud sync default), fallback to default account
    applescript_fallback = f'''
    tell application "Notes"
        activate
        tell default account
            make new note at folder "Notes" with properties {{body:"{content}"}}
        end tell
    end tell
    '''

    try:
        process = subprocess.run(['osascript', '-e', applescript_fallback], capture_output=True, text=True)
        if process.returncode != 0:
            # Try the fallback if default account fails
            subprocess.run(['osascript', '-e', applescript])
        speak_func("The note has been saved successfully.")
    except Exception as e:
        speak_func("Sorry sir, I couldn't save the note.")
        print(f"Notes Error: {e}")

def create_reminder(content, speak_func):
    speak_func(f"Adding '{content}' to your Reminders, sir.")

    # AppleScript to create a reminder natively on macOS
    applescript = f'''
    tell application "Reminders"
        tell default list
            make new reminder with properties {{name:"{content}"}}
        end tell
    end tell
    '''

    try:
        subprocess.run(['osascript', '-e', applescript], capture_output=True, text=True)
        speak_func("Reminder added successfully.")
    except Exception as e:
        speak_func("Sorry sir, I couldn't add the reminder.")
        print(f"Reminders Error: {e}")

def timer_alert(speak_func):
    # Play a native Mac sound to indicate timer completion
    subprocess.run(["afplay", "/System/Library/Sounds/Glass.aiff"])
    speak_func("Sir, the timer you set has finished!")

def set_timer(seconds, speak_func):
    try:
        seconds = int(seconds)
        mins = seconds // 60
        secs = seconds % 60
        time_spoken = f"{mins} minutes and {secs} seconds" if mins > 0 else f"{seconds} seconds"

        speak_func(f"Timer set for {time_spoken}, sir.")

        t = threading.Timer(seconds, timer_alert, args=[speak_func])
        t.start()
    except ValueError:
        speak_func("Sir, I couldn't understand the duration for the timer. Please specify in minutes or seconds.")
