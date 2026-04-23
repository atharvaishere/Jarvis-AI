import sys
import threading
import time
import math
import psutil
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
    QWidget, QLabel, QTextEdit, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer, QPoint, QPointF, QRectF
from PyQt6.QtGui import QFont, QColor, QPalette, QPainter, QRadialGradient, QPen, QBrush

# Import Jarvis state and main logic
from core.state import state
import main as jarvis_main

class GlowingOrb(QWidget):
    """A 2026-style AI glowing orb visualizer using custom antialiased rendering."""
    def __init__(self):
        super().__init__()
        self.setFixedSize(250, 250)
        self.pulse = 0
        self.pulse_dir = 1
        self.rotation = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(20) # Super smooth 50 FPS

    def animate(self):
        status = state.get_status()
        self.rotation = (self.rotation + 2) % 360
        
        # Adjust animation intensity based on AI state
        if "SPEAKING" in status:
            step = 8.0
            max_pulse = 50
        elif "LISTENING" in status:
            step = 3.0
            max_pulse = 30
        elif "THINKING" in status:
            step = 1.5
            max_pulse = 20
        else:
            step = 0.5
            max_pulse = 10
            
        self.pulse += step * self.pulse_dir
        if self.pulse > max_pulse:
            self.pulse_dir = -1
            self.pulse = max_pulse
        elif self.pulse < 0:
            self.pulse_dir = 1
            self.pulse = 0
            
        self.update() # Trigger a repaint

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        center = self.rect().center()
        cx, cy = float(center.x()), float(center.y())
        base_radius = 50.0
        current_radius = base_radius + self.pulse
        
        # Color transitions based on state
        status = state.get_status()
        if "SPEAKING" in status:
            base_color = QColor(0, 243, 255, 180)  # Neon Cyan
        elif "LISTENING" in status:
            base_color = QColor(255, 0, 128, 180)  # Neon Pink
        elif "THINKING" in status:
            base_color = QColor(128, 0, 255, 180)  # Deep Purple
        else:
            base_color = QColor(100, 100, 120, 80) # Sleep Grey

        # Outer Glow (Radial Gradient)
        gradient = QRadialGradient(cx, cy, current_radius)
        gradient.setColorAt(0, base_color)
        gradient.setColorAt(1, QColor(0, 0, 0, 0))
        
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(gradient))
        painter.drawEllipse(center, int(current_radius), int(current_radius))
        
        # Inner Core Ring
        pen = QPen(base_color)
        pen.setWidth(2)
        painter.setPen(pen)
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawEllipse(center, int(base_radius), int(base_radius))

class ModernCard(QWidget):
    """A sleek, glassmorphism-style rounded card widget."""
    def __init__(self, layout):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setStyleSheet("""
            QWidget {
                background-color: #12121a;
                border: 1px solid #2a2a35;
                border-radius: 20px;
            }
        """)
        
        # Soft shadow
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(10)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.setGraphicsEffect(shadow)
        
        self.setLayout(layout)

class ModernJarvisHUD(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Jarvis AI | 2026 Edition")
        self.resize(850, 650)

        # Frameless and translucent dark background
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        font_family = "Helvetica Neue"

        # Main Central Widget wrapping everything in a beautifully rounded dark container
        self.central_container = QWidget()
        self.central_container.setStyleSheet("""
            QWidget#MainContainer {
                background-color: #080A10;
                border: 1px solid #1a1a24;
                border-radius: 30px;
            }
        """)
        self.central_container.setObjectName("MainContainer")
        self.setCentralWidget(self.central_container)

        main_layout = QVBoxLayout(self.central_container)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(20)

        # 1. TOP HEADER ROW (Title & Close Button)
        header_layout = QHBoxLayout()
        title_label = QLabel("J.A.R.V.I.S.")
        title_label.setFont(QFont(font_family, 28, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #ffffff; background: transparent; border: none;")
        header_layout.addWidget(title_label)

        header_layout.addStretch()

        self.close_btn = QLabel("⏻") # Power icon
        self.close_btn.setFont(QFont(font_family, 24))
        self.close_btn.setFixedSize(40, 40)
        self.close_btn.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.close_btn.setStyleSheet("""
            QLabel {
                color: #ff3366; background-color: #1a1015;
                border-radius: 20px; border: 1px solid #331520;
            }
            QLabel:hover { background-color: #ff3366; color: white; }
        """)
        self.close_btn.mousePressEvent = self.close_app
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        header_layout.addWidget(self.close_btn)

        main_layout.addLayout(header_layout)

        # 2. MIDDLE SECTION (Vitals, Orb, Status)
        mid_layout = QHBoxLayout()
        mid_layout.setSpacing(20)

        # Left Vitals Card
        vitals_inner = QVBoxLayout()
        vitals_title = QLabel("SYSTEM METRICS")
        vitals_title.setFont(QFont(font_family, 10, QFont.Weight.Bold))
        vitals_title.setStyleSheet("color: #8a8a9e; background: transparent; border: none;")
        
        self.cpu_label = QLabel("CPU: 0%")
        self.ram_label = QLabel("RAM: 0%")
        self.bat_label = QLabel("BATT: 0%")
        for lbl in [self.cpu_label, self.ram_label, self.bat_label]:
            lbl.setFont(QFont(font_family, 16))
            lbl.setStyleSheet("color: #00f3ff; background: transparent; border: none; margin-top: 10px;")
            
        vitals_inner.addWidget(vitals_title)
        vitals_inner.addWidget(self.cpu_label)
        vitals_inner.addWidget(self.ram_label)
        vitals_inner.addWidget(self.bat_label)
        vitals_inner.addStretch()
        
        self.vitals_card = ModernCard(vitals_inner)
        self.vitals_card.setFixedWidth(200)
        mid_layout.addWidget(self.vitals_card)

        # Center AI Orb
        orb_layout = QVBoxLayout()
        orb_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.orb = GlowingOrb()
        orb_layout.addWidget(self.orb)
        
        self.status_label = QLabel("INITIALIZING...")
        self.status_label.setFont(QFont(font_family, 14, QFont.Weight.Bold))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #ffffff; background: transparent; border: none; letter-spacing: 2px; margin-top: 10px;")
        orb_layout.addWidget(self.status_label)
        
        mid_layout.addLayout(orb_layout)

        # Right Action Card (Date/Time)
        right_inner = QVBoxLayout()
        date_title = QLabel("DATE & TIME")
        date_title.setFont(QFont(font_family, 10, QFont.Weight.Bold))
        date_title.setStyleSheet("color: #8a8a9e; background: transparent; border: none;")
        
        self.time_label = QLabel("00:00")
        self.time_label.setFont(QFont(font_family, 26, QFont.Weight.Bold))
        self.time_label.setStyleSheet("color: #ffffff; background: transparent; border: none; margin-top: 5px;")
        
        self.date_label = QLabel("---")
        self.date_label.setFont(QFont(font_family, 12))
        self.date_label.setStyleSheet("color: #00f3ff; background: transparent; border: none;")
        
        right_inner.addWidget(date_title)
        right_inner.addWidget(self.time_label)
        right_inner.addWidget(self.date_label)
        right_inner.addStretch()
        
        self.right_card = ModernCard(right_inner)
        self.right_card.setFixedWidth(200)
        mid_layout.addWidget(self.right_card)

        main_layout.addLayout(mid_layout)

        # 3. BOTTOM TERMINAL (Clean Chat UI)
        chat_layout = QVBoxLayout()
        chat_title = QLabel("RECENT ACTIVITY")
        chat_title.setFont(QFont(font_family, 10, QFont.Weight.Bold))
        chat_title.setStyleSheet("color: #8a8a9e; background: transparent; border: none; padding-left: 10px;")
        
        self.chat_view = QTextEdit()
        self.chat_view.setReadOnly(True)
        self.chat_view.setFont(QFont(font_family, 13))
        self.chat_view.setStyleSheet("""
            QTextEdit {
                background-color: transparent;
                color: #e0e0e0;
                border: none;
                padding: 10px;
                line-height: 1.5;
            }
        """)
        
        chat_layout.addWidget(chat_title)
        chat_layout.addWidget(self.chat_view)
        self.chat_card = ModernCard(chat_layout)
        self.chat_card.setFixedHeight(200)
        
        main_layout.addWidget(self.chat_card)

        # Timers
        self.ui_timer = QTimer()
        self.ui_timer.timeout.connect(self.update_ui)
        self.ui_timer.start(50)

        self.sys_timer = QTimer()
        self.sys_timer.timeout.connect(self.update_vitals)
        self.sys_timer.start(1000)

        self.last_log_count = 0
        self.drag_pos = None

        # Start Jarvis Core
        self.jarvis_thread = threading.Thread(target=jarvis_main.chat_with_jarvis, args=(True,), daemon=True)
        self.jarvis_thread.start()

    def update_ui(self):
        status = state.get_status()
        self.status_label.setText(status.replace("...", "").upper())

        logs = state.get_logs()
        if len(logs) > self.last_log_count:
            for log in logs[self.last_log_count:]:
                # Format You/Jarvis differently
                if log.startswith("You:"):
                    fmt = f'<div style="color:#8a8a9e; margin: 5px 0;">{log}</div>'
                elif log.startswith("Jarvis:"):
                    fmt = f'<div style="color:#00f3ff; margin: 5px 0;"><b>{log}</b></div>'
                else:
                    fmt = f'<div style="color:#ffffff; margin: 5px 0;">{log}</div>'
                self.chat_view.append(fmt)
            self.last_log_count = len(logs)
            scrollbar = self.chat_view.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())

    def update_vitals(self):
        self.cpu_label.setText(f"CPU: {psutil.cpu_percent()}%")
        self.ram_label.setText(f"RAM: {psutil.virtual_memory().percent}%")
        battery = psutil.sensors_battery()
        if battery:
            self.bat_label.setText(f"BATT: {battery.percent}% {'⚡' if battery.power_plugged else ''}")
        
        self.time_label.setText(time.strftime("%H:%M"))
        self.date_label.setText(time.strftime("%d %b %Y").upper())

    def close_app(self, event):
        jarvis_main.JARVIS_ACTIVE = False
        sys.exit(0)

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
    hud = ModernJarvisHUD()
    hud.show()
    sys.exit(app.exec())
