import sys
import threading
import time
import random
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTextEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QColor, QPalette

# Import Jarvis state and main logic
from core.state import state
import main as jarvis_main

class AudioVisualizer(QWidget):
    """A simulated audio visualizer for the center of the HUD."""
    def __init__(self):
        super().__init__()
        self.bars = []
        layout = QHBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(5)

        # Create 15 vertical progress bars (sound bars)
        for i in range(15):
            bar = QProgressBar()
            bar.setOrientation(Qt.Orientation.Vertical)
            bar.setTextVisible(False)
            bar.setFixedSize(12, 100)

            # Styling for the neon cyan bars
            bar.setStyleSheet("""
                QProgressBar {
                    background-color: #111111;
                    border: 1px solid #00f3ff;
                    border-radius: 2px;
                }
                QProgressBar::chunk {
                    background-color: #00f3ff;
                }
            """)
            self.bars.append(bar)
            layout.addWidget(bar)

        self.setLayout(layout)

        # Timer for animating the bars
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate_bars)
        self.timer.start(80) # 80ms refresh rate for smooth jumping

    def animate_bars(self):
        current_status = state.get_status()

        if "SPEAKING" in current_status:
            # High intensity, fast jumps
            for bar in self.bars:
                bar.setValue(random.randint(40, 100))
        elif "LISTENING" in current_status:
            # Medium intensity, undulating
            for bar in self.bars:
                bar.setValue(random.randint(10, 60))
        elif "THINKING" in current_status:
            # Smooth spinning or pulsing wave (we'll just do a low pulse)
            for i, bar in enumerate(self.bars):
                offset = (time.time() * 10 + i) % 15
                val = 40 if offset < 3 else 10
                bar.setValue(int(val))
        else:
            # Sleep or idle - flatline with tiny blips
            for bar in self.bars:
                bar.setValue(random.randint(0, 10))

class IronManHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("J.A.R.V.I.S. SYSTEM INTERFACE")
        self.resize(800, 600)

        # Set Frameless Window and Dark Theme
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet("background-color: #050505; color: #00f3ff; border: 2px solid #00f3ff;")

        # Main Widget and Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # 1. HEADER
        self.header_label = QLabel("J.A.R.V.I.S. // MK I")
        self.header_label.setFont(QFont("Courier New", 24, QFont.Weight.Bold))
        self.header_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header_label.setStyleSheet("border: none; padding-bottom: 20px; letter-spacing: 5px;")
        main_layout.addWidget(self.header_label)

        # 2. MIDDLE SECTION (Left: Vitals, Center: Visualizer, Right: System Info)
        mid_layout = QHBoxLayout()

        # Left Panel (Vitals)
        self.vitals_label = QLabel("SYSTEM VITALS:\n\nCPU: 0%\nRAM: 0%\nBATTERY: 0%")
        self.vitals_label.setFont(QFont("Courier New", 14))
        self.vitals_label.setStyleSheet("border: 1px solid #005555; padding: 10px; background-color: #0a0a0a;")
        self.vitals_label.setFixedWidth(200)
        mid_layout.addWidget(self.vitals_label)

        # Center Panel (Visualizer)
        self.visualizer = AudioVisualizer()
        self.visualizer.setStyleSheet("border: none;")
        mid_layout.addWidget(self.visualizer)

        # Right Panel (Close Button & Date)
        right_panel = QVBoxLayout()
        self.date_label = QLabel("DATE: --/--/----")
        self.date_label.setFont(QFont("Courier New", 14))
        self.date_label.setStyleSheet("border: 1px solid #005555; padding: 10px; background-color: #0a0a0a;")

        self.close_btn = QLabel("[ SHUT DOWN ]")
        self.close_btn.setFont(QFont("Courier New", 14, QFont.Weight.Bold))
        self.close_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.close_btn.setStyleSheet("color: #ff0055; border: 1px solid #ff0055; padding: 10px;")
        self.close_btn.mousePressEvent = self.close_app # Make it clickable
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)

        right_panel.addWidget(self.date_label)
        right_panel.addStretch()
        right_panel.addWidget(self.close_btn)
        mid_layout.addLayout(right_panel)

        main_layout.addLayout(mid_layout)

        # 3. TERMINAL LOGS
        self.terminal = QTextEdit()
        self.terminal.setReadOnly(True)
        self.terminal.setFont(QFont("Courier New", 12))
        self.terminal.setStyleSheet("""
            QTextEdit {
                background-color: #020202;
                color: #00f3ff;
                border: 1px solid #005555;
                padding: 10px;
            }
        """)
        main_layout.addWidget(self.terminal)

        # 4. CURRENT STATUS FOOTER
        self.status_label = QLabel("[ STATUS: INITIALIZING... ]")
        self.status_label.setFont(QFont("Courier New", 16, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("border: none; padding-top: 10px;")
        main_layout.addWidget(self.status_label)

        # Timers for updating UI elements
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(100) # Update logs and status every 100ms

        self.sys_timer = QTimer()
        self.sys_timer.timeout.connect(self.update_vitals)
        self.sys_timer.start(2000) # Update CPU/Battery every 2 seconds

        self.last_log_count = 0

        # Dragging variables for frameless window
        self.drag_pos = None

        # Start Jarvis Thread
        self.jarvis_thread = threading.Thread(target=jarvis_main.chat_with_jarvis, args=(True,), daemon=True)
        self.jarvis_thread.start()

    def update_ui(self):
        # Update Status
        current_status = state.get_status()
        self.status_label.setText(f"[ STATUS: {current_status} ]")

        # Update Logs
        logs = state.get_logs()
        if len(logs) > self.last_log_count:
            # Append new logs
            for log in logs[self.last_log_count:]:
                self.terminal.append(log)
            self.last_log_count = len(logs)

            # Scroll to bottom
            scrollbar = self.terminal.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def update_vitals(self):
        cpu = psutil.cpu_percent()
        ram = psutil.virtual_memory().percent
        battery = psutil.sensors_battery()
        batt_str = f"{battery.percent}%" if battery else "N/A"

        self.vitals_label.setText(f"SYSTEM VITALS:\n\nCPU: {cpu}%\nRAM: {ram}%\nBATT: {batt_str}")
        self.date_label.setText(time.strftime("TIME: %H:%M:%S\nDATE: %d %b %Y"))

    def close_app(self, event):
        # Cleanly shutdown Jarvis loop and exit GUI
        jarvis_main.JARVIS_ACTIVE = False
        sys.exit(0)

    # Allow dragging the frameless window
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos is not None:
            delta = event.globalPosition().toPoint() - self.drag_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.drag_pos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        self.drag_pos = None

if __name__ == "__main__":
    app = QApplication(sys.exit(0) if sys.flags.interactive else sys.argv)
    hud = IronManHUD()
    hud.show()
    sys.exit(app.exec())
