import subprocess
import difflib

def run_apple_shortcut(target, speak_func):
    speak_func(f"Looking for the shortcut {target}, sir...")

    try:
        # Get list of all installed shortcuts on the Mac
        output = subprocess.check_output(['shortcuts', 'list'], text=True)
        shortcuts = [line.strip() for line in output.split('\n') if line.strip()]

        if not shortcuts:
            speak_func("Sir, you don't have any Apple Shortcuts installed.")
            return

        # Fuzzy match to find the closest shortcut name
        matches = difflib.get_close_matches(target, shortcuts, n=1, cutoff=0.5)

        if matches:
            actual_shortcut = matches[0]
            speak_func(f"Running the {actual_shortcut} shortcut now.")
            # Run the matched shortcut
            subprocess.run(['shortcuts', 'run', actual_shortcut])
        else:
            speak_func(f"Sorry sir, I couldn't find any shortcut matching '{target}'.")

    except subprocess.CalledProcessError:
        speak_func("There was an error accessing your Apple Shortcuts, sir.")
    except Exception as e:
        print(f"Shortcut Error: {e}")
        speak_func("An unexpected error occurred while trying to run the shortcut.")
