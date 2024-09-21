import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QPainter, QColor, QBrush, QIcon, QAction
from PyQt6.QtCore import Qt, QRect, QSize, QPoint
import os

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setFixedSize(320, 640)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.background_color = QColor(0, 0, 0, 180)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Close button (red)
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(16, 16)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-image: url('Bin/button_close.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
                transition: background-image 1.5s ease-in-out;
            }
            QPushButton:hover {
                background-image: url('Bin/button_close_hover.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
            }
        """)
        self.close_button.clicked.connect(self.close)

        # Minimize button (blue)
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedSize(16, 16)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-image: url('Bin/button_minimize.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
                transition: background-image 1.5s ease-in-out;
            }
            QPushButton:hover {
                background-image: url('Bin/button_minimize_hover.png');
                background-repeat: no-repeat;
                background-position: center;
                border-radius: 8px;
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_to_tray)

        self.minimize_button.move(8, 8)
        self.close_button.move(32, 8)


        self.clicked = False
        self.old_geometry = self.geometry()

        self.dragging = False
        self.drag_position = QPoint(0, 0)

        self.tray_icon = QSystemTrayIcon(self)

        icon_path = os.path.join(os.path.dirname(__file__), "Bin/icon.png")

        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))
        else:
            print(f"Icon not found at path: {icon_path}")
            self.tray_icon.setIcon(QIcon())

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