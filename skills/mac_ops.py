import os
import time
import subprocess
import pyautogui

def open_app(target, speak_func):
    # Fallback safety: If LLM accidentally sends a website to open_app
    if '.com' in target.lower() or target.lower() in ['youtube', 'google']:
        import webbrowser
        clean_site = target.lower().replace('.com', '')
        speak_func(f"Opening {clean_site} for you, sir!")
        webbrowser.open(f"https://www.{clean_site}.com")
        return

    # Dictionary to normalize common misspoken or alternative app names
    APP_ALIASES = {
        'message': 'Messages',
        'messages': 'Messages',
        'imessage': 'Messages',
        'music app': 'Music',
        'apple music': 'Music',
        'chrome': 'Google Chrome',
        'settings': 'System Settings',
        'system preferences': 'System Settings',
        'safari browser': 'Safari'
    }

    clean_target = target.lower().strip()
    actual_app_name = APP_ALIASES.get(clean_target, target)

    speak_func(f"Opening {actual_app_name} for you, sir!")
    os.system(f'open -a "{actual_app_name}"')

def close_app(target, speak_func):
    speak_func(f"Closing {target}, sir.")
    # Using osascript to gracefully quit the application
    os.system(f"osascript -e 'tell application \"{target}\" to quit'")

def take_screenshot(speak_func):
    filepath = os.path.expanduser(f"~/Desktop/Jarvis_Screenshot_{int(time.time())}.png")
    output = subprocess.getoutput(f"screencapture {filepath}")
    if "could not create image" in output.lower() or "error" in output.lower():
        speak_func("Sir, please allow Terminal in Mac Screen Recording privacy settings to take screenshots.")
    else:
        speak_func("Screenshot saved to your Desktop, sir!")

def mac_control(target, speak_func):
    if target == 'volume_max':
        os.system("osascript -e 'set volume output volume 100'")
        speak_func("Volume is at maximum!")
    elif target == 'volume_min':
        os.system("osascript -e 'set volume output volume 0'")
        speak_func("Volume minimized.")
    elif target == 'volume_up':
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) + 20)'")
        speak_func("Turned the volume up.")
    elif target == 'volume_down':
        os.system("osascript -e 'set volume output volume ((output volume of (get volume settings)) - 20)'")
        speak_func("Turned the volume down.")
    elif target == 'mute':
        os.system("osascript -e 'set volume with output muted'")
        speak_func("Muted the audio.")
    elif target == 'brightness_up':
        status = os.system("osascript -e 'tell application \"System Events\" to key code 144' 2>/dev/null")
        if status != 0:
            speak_func("Sir, please allow Terminal in Mac Accessibility settings to change brightness.")
        else:
            speak_func("Brightness increased.")
    elif target == 'brightness_down':
        status = os.system("osascript -e 'tell application \"System Events\" to key code 145' 2>/dev/null")
        if status != 0:
            speak_func("Sir, please allow Terminal in Mac Accessibility settings to change brightness.")
        else:
            speak_func("Brightness decreased.")
    elif target == 'play_pause':
        pyautogui.press('playpause')
        speak_func("Toggled media playback.")
    elif target in ['focus_on', 'focus_off']:
        os.system('open "x-apple.systempreferences:com.apple.preference.notifications"')
        speak_func("I've opened the Focus settings for you, sir. Just toggle it right there.")
    elif target == 'minimize_window':
        # Simulates Cmd+M
        os.system("osascript -e 'tell application \"System Events\" to keystroke \"m\" using command down'")
        speak_func("Minimized the active window.")
    elif target == 'hide_all':
        # Simulates F11 (Show Desktop)
        os.system("osascript -e 'tell application \"System Events\" to key code 103'")
        speak_func("Showing desktop.")

def hardware_control(target, speak_func):
    # Dynamically find the Wi-Fi port (usually en0)
    wifi_port = subprocess.getoutput("networksetup -listallhardwareports | awk '/Wi-Fi/ {getline; print $2}'").strip()
    if not wifi_port:
        wifi_port = "en0"

    if target == 'wifi_on':
        os.system(f"networksetup -setairportpower {wifi_port} on")
        speak_func("Wi-Fi has been turned on, sir.")

    elif target == 'wifi_off':
        os.system(f"networksetup -setairportpower {wifi_port} off")
        speak_func("Wi-Fi has been turned off, sir.")

    elif target == 'sleep':
        speak_func("Putting the Mac to sleep. Goodnight, sir.")
        time.sleep(1) # Give it a second to speak before sleeping
        os.system("pmset sleepnow")

    elif target == 'restart':
        speak_func("Restarting the system now, sir.")
        os.system('osascript -e \'tell application "System Events" to restart\'')

    elif target == 'shutdown':
        speak_func("Shutting down the Mac completely. Farewell, sir.")
        os.system('osascript -e \'tell application "System Events" to shut down\'')

