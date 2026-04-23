import time
import threading
import psutil
from core.speak import speak

def battery_monitor():
    """Continuously monitors battery and proactively warns the user if it gets low."""
    low_battery_warned = False

    while True:
        try:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                is_plugged = battery.power_plugged

                # Warn if battery drops to 20% or below and is not charging
                if percent <= 20 and not is_plugged and not low_battery_warned:
                    # Speak proactively without being asked
                    speak(f"Excuse me sir, your Mac battery is down to {percent} percent. I highly recommend plugging it in.")
                    low_battery_warned = True

                # Reset the warning state if the user plugs it in or it charges above 20%
                if is_plugged or percent > 20:
                    low_battery_warned = False

        except Exception as e:
            print(f"Proactive Battery Monitor Error: {e}")

        # Check the battery status every 60 seconds
        time.sleep(60)

def start_proactive_monitors():
    """Starts all background monitoring threads for Jarvis to speak proactively."""
    threading.Thread(target=battery_monitor, daemon=True).start()
