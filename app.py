import rumps
import threading
import sys

# Import our Jarvis logic
import main as jarvis_main

class JarvisApp(rumps.App):
    def __init__(self):
        # Initial status is asleep/offline (🤖)
        super(JarvisApp, self).__init__(name="Jarvis", title="🤖")
        self.jarvis_thread = None
        self.menu = ["Start Jarvis", "Stop Jarvis", rumps.separator, "Quit App"]

    @rumps.clicked("Start Jarvis")
    def start_jarvis(self, _):
        if self.jarvis_thread is None or not self.jarvis_thread.is_alive():
            self.title = "🟢" # Change icon to active
            # Run Jarvis in a background thread so the Menu Bar doesn't freeze
            self.jarvis_thread = threading.Thread(target=jarvis_main.chat_with_jarvis, args=(True,), daemon=True)
            self.jarvis_thread.start()
            rumps.notification(title="Jarvis AI", subtitle="Systems Online", message="Jarvis is now listening in the background.")
        else:
            rumps.notification(title="Jarvis AI", subtitle="Status", message="Jarvis is already running.")

    @rumps.clicked("Stop Jarvis")
    def stop_jarvis(self, _):
        if self.jarvis_thread and self.jarvis_thread.is_alive():
            # Signal the background loop to stop gracefully
            jarvis_main.JARVIS_ACTIVE = False
            self.title = "💤" # Change icon to sleeping
            rumps.notification(title="Jarvis AI", subtitle="Systems Offline", message="Jarvis has been put to sleep.")
        else:
            rumps.notification(title="Jarvis AI", subtitle="Status", message="Jarvis is already stopped.")

    @rumps.clicked("Quit App")
    def quit_app(self, _):
        # Stop Jarvis if running before completely exiting the app
        jarvis_main.JARVIS_ACTIVE = False
        rumps.quit_application()

if __name__ == "__main__":
    # Start the macOS Menu Bar app
    app = JarvisApp()
    app.quit_button = None # Disable default quit to use our custom one
    app.run()
