import speech_recognition as sr
import time
from core.state import state

def listen(quiet=False, active_timeout=240):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            if not quiet:
                print("\n🎤 Listening...")
                state.set_status("LISTENING...")
            else:
                state.set_status("SLEEPING... (Say 'Jarvis' to wake me)")

            # Hardcode average threshold to completely remove the 0.1s-0.5s calibration delay
            recognizer.energy_threshold = 3000
            recognizer.dynamic_energy_threshold = True

            # 1.2 seconds of silence required to cut you off (a perfect balance between not cutting you off and not waiting forever)
            recognizer.pause_threshold = 1.2

            try:
                # Use shorter timeout when sleeping (quiet), and longer when active
                current_timeout = 3 if quiet else active_timeout
                audio = recognizer.listen(source, timeout=current_timeout, phrase_time_limit=15)
                text = recognizer.recognize_google(audio, language="en-IN")
                return text
            except sr.WaitTimeoutError:
                return "TIMEOUT"
            except sr.UnknownValueError:
                return "UNKNOWN"
            except sr.RequestError:
                return None
            except Exception:
                return None

    except AttributeError:
        # Catches the specific PyAudio 'NoneType' object has no attribute 'close' bug
        # This happens when Mac CoreAudio drops the mic temporarily due to heavy CPU load or Camera conflicts
        print("\n[Hardware Warning]: Microphone temporarily locked. Re-initializing...")
        time.sleep(2)  # Give macOS time to free up the hardware
        return "UNKNOWN"
    except Exception as e:
        print(f"\n[Mic Error]: {e}")
        time.sleep(2)
        return "UNKNOWN"

