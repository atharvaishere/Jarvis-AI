import webbrowser
import pywhatkit
import wikipedia

def open_website(target, speak_func):
    speak_func(f"Opening {target}!")
    webbrowser.open(f"https://www.{target}")

def play_youtube(target, speak_func):
    speak_func(f"Playing {target} on YouTube right away!")
    pywhatkit.playonyt(target)

def search_wikipedia(target, speak_func):
    speak_func(f"Let me check Wikipedia for {target}...")
    try:
        results = wikipedia.summary(target, sentences=2)
        print(f"\nWikipedia: {results}")
        speak_func(f"According to Wikipedia, {results}")
        return results
    except wikipedia.exceptions.DisambiguationError:
        speak_func("There are too many results for that, sir. Can you be more specific?")
    except wikipedia.exceptions.PageError:
        speak_func("I couldn't find anything about that on Wikipedia.")
    return None
