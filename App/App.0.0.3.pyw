from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu, QGraphicsOpacityEffect
from PyQt6.QtGui import QPainter, QColor, QBrush, QIcon, QAction
from PyQt6.QtCore import Qt, QRect, QPropertyAnimation, QEasingCurve
import sys, os

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setFixedSize(320, 640)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.background_color = QColor(0, 0, 0, 180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Close button
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(16, 16)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-image: url('Bin/button_close.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
            }
        """)
        self.close_button.clicked.connect(self.close)

        # Add opacity effect and animation for hover
        self.close_button_opacity = QGraphicsOpacityEffect(self.close_button)
        self.close_button.setGraphicsEffect(self.close_button_opacity)

        self.close_fade_in = QPropertyAnimation(self.close_button_opacity, b"opacity")
        self.close_fade_out = QPropertyAnimation(self.close_button_opacity, b"opacity")
        
        # Adjust animation durations (in milliseconds)
        self.close_fade_in.setDuration(500)  # 500 ms fade-in
        self.close_fade_out.setDuration(500)  # 500 ms fade-out
        
        self.close_fade_in.setStartValue(0.5)  # Start at 50% opacity
        self.close_fade_in.setEndValue(1.0)   # End at 100% opacity
        self.close_fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.close_fade_out.setStartValue(1.0)  # Start at 100% opacity
        self.close_fade_out.setEndValue(0.5)    # End at 50% opacity
        self.close_fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Connect hover events directly to the close button
        self.close_button.enterEvent = self.on_close_button_hover
        self.close_button.leaveEvent = self.on_close_button_leave

        # Minimize button
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedSize(16, 16)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-image: url('Bin/button_minimize.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_to_tray)

        # Add opacity effect and animation for minimize button hover
        self.minimize_button_opacity = QGraphicsOpacityEffect(self.minimize_button)
        self.minimize_button.setGraphicsEffect(self.minimize_button_opacity)

        self.minimize_fade_in = QPropertyAnimation(self.minimize_button_opacity, b"opacity")
        self.minimize_fade_out = QPropertyAnimation(self.minimize_button_opacity, b"opacity")
        
        # Adjust animation durations (in milliseconds)
        self.minimize_fade_in.setDuration(500)  # 500 ms fade-in
        self.minimize_fade_out.setDuration(500)  # 500 ms fade-out
        
        self.minimize_fade_in.setStartValue(0.5)  # Start at 50% opacity
        self.minimize_fade_in.setEndValue(1.0)    # End at 100% opacity
        self.minimize_fade_in.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.minimize_fade_out.setStartValue(1.0)  # Start at 100% opacity
        self.minimize_fade_out.setEndValue(0.5)    # End at 50% opacity
        self.minimize_fade_out.setEasingCurve(QEasingCurve.Type.InOutQuad)

        # Connect hover events directly to the minimize button
        self.minimize_button.enterEvent = self.on_minimize_button_hover
        self.minimize_button.leaveEvent = self.on_minimize_button_leave

        # Position buttons
        self.minimize_button.move(8, 8)
        self.close_button.move(32, 8)

        # Tray icon setup
        self.tray_icon = QSystemTrayIcon(self)
        icon_path = os.path.join(os.path.dirname(__file__), "Bin/icon.png")
        self.tray_icon.setIcon(QIcon(icon_path) if os.path.exists(icon_path) else QIcon())

        tray_menu = QMenu()
        restore_action = QAction("Show", self)
        restore_action.triggered.connect(self.restore_from_tray)
        tray_menu.addAction(restore_action)

        exit_action = QAction("Close", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_click)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 8, 8)

    def on_close_button_hover(self, event):
        self.close_fade_in.start()

    def on_close_button_leave(self, event):
        self.close_fade_out.start()

    def on_minimize_button_hover(self, event):
        self.minimize_fade_in.start()

    def on_minimize_button_leave(self, event):
        self.minimize_fade_out.start()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.dragging = False

    def minimize_to_tray(self):
        self.hide()
        self.tray_icon.show()

    def restore_from_tray(self):
        self.show()
        self.tray_icon.hide()

    def on_tray_icon_click(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.restore_from_tray()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomWindow()
    window.show()
    sys.exit(app.exec())
