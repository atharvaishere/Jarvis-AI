import pyjokes

def tell_joke(speak_func):
    joke = pyjokes.get_joke()
    print(f"Joke: {joke}")
    speak_func(joke)
    return joke
