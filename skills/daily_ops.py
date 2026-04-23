import datetime
import psutil
import requests

def get_time(speak_func):
    current_time = datetime.datetime.now().strftime("%I:%M %p")
    speak_func(f"Sir, the time right now is {current_time}.")
    return current_time

def get_date(speak_func):
    current_date = datetime.datetime.now().strftime("%B %d, %Y")
    speak_func(f"Today's date is {current_date}.")
    return current_date

def get_battery(speak_func):
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        is_plugged = battery.power_plugged
        plug_status = "and it's charging" if is_plugged else "and it's on battery power"
        speak_func(f"Your Mac is at {percent} percent battery, {plug_status}.")
        return f"{percent}%"
    else:
        speak_func("Sorry sir, I couldn't read the battery sensor.")
        return None

def get_weather(speak_func):
    speak_func("Checking the sky for you, sir...")
    try:
        weather = requests.get("https://wttr.in/?format=%l:+%C,+with+a+temperature+of+%t").text.strip()
        weather = weather.replace('+', 'plus ').replace('-', 'minus ').replace('Â', '').replace('°C', ' degrees Celsius').replace('°F', ' degrees Fahrenheit')
        print(f"Weather: {weather}")
        speak_func(f"The weather is {weather}")
        return weather
    except:
        speak_func("Sorry sir, the weather service is down right now.")
        return None
