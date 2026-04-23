import threading

class JarvisState:
    def __init__(self):
        self.status = "OFFLINE"
        self.logs = []
        self.lock = threading.Lock()

    def set_status(self, new_status):
        with self.lock:
            self.status = new_status

    def get_status(self):
        with self.lock:
            return self.status

    def add_log(self, log_msg):
        with self.lock:
            self.logs.append(log_msg)
            # Keep only the last 100 logs to save memory
            if len(self.logs) > 100:
                self.logs.pop(0)

    def get_logs(self):
        with self.lock:
            # Return a copy of the list
            return list(self.logs)

# Global singleton instance for all modules to access
state = JarvisState()
