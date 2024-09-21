import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QPainter, QColor, QBrush, QIcon, QAction
from PyQt6.QtCore import Qt, QRect, QSize, QPoint
import os

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Window configurations
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)  # No title bar and doesn't appear in the taskbar
        self.setFixedSize(240, 500)  # Fixed size
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Transparent background

        # Setting the background color with 80% opacity
        self.background_color = QColor(0, 0, 0, 204)  # Black with 80% opacity (204/255)

        # Basic layout to add buttons
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Close button (red)
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: rgba(255, 192, 203, 1);
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightcoral;
            }
        """)
        self.close_button.clicked.connect(self.close)

        # Minimize button (blue)
        self.minimize_button = QPushButton(self)
        self.minimize_button.setFixedSize(20, 20)
        self.minimize_button.setStyleSheet("""
            QPushButton {
                background-color: blue;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightblue;
            }
        """)
        self.minimize_button.clicked.connect(self.minimize_to_tray)

        # Button positioning
        self.close_button.move(210, 10)  # Position in the upper right corner
        self.minimize_button.move(180, 10)  # Position to the left of the close button

        # Click event for maximizing
        self.clicked = False  # Flag to control the maximization state
        self.old_geometry = self.geometry()

        # Variables for drag and drop
        self.dragging = False  # Drag state control
        self.drag_position = QPoint(0, 0)  # Initial mouse position when dragging

        # System Tray Icon - use the custom icon (green drop)
        self.tray_icon = QSystemTrayIcon(self)

        # Sets the absolute path to the icon
        icon_path = os.path.join(os.path.dirname(__file__), "Bin/icon.png")

        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))  # Load the icon correctly
        else:
            print(f"Icon not found at path: {icon_path}")
            self.tray_icon.setIcon(QIcon())  # Uses an empty icon if the icon is not found

        # Creating the tray icon menu
        tray_menu = QMenu()

        # Action to restore the window from the tray
        restore_action = QAction("Show", self)
        restore_action.triggered.connect(self.restore_from_tray)
        tray_menu.addAction(restore_action)

        # Action to exit the application from the tray
        exit_action = QAction("Close", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)

        # Connect the menu to the tray icon
        self.tray_icon.setContextMenu(tray_menu)

        # Connect the double click to restore the window
        self.tray_icon.activated.connect(self.on_tray_icon_click)

    def paintEvent(self, event):
        # Paint the rounded background of the window
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 15, 15)  # Rounded corners

    def mousePressEvent(self, event):
        # Start dragging when the left mouse button is pressed
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Updates the window position as the mouse is moved
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Ends the drag when the mouse button is released
        self.dragging = False

    def minimize_to_tray(self):
        # Minimizes the window and hides it, showing the icon in the tray
        self.hide()
        self.tray_icon.show()

    def restore_from_tray(self):
        # Restores the window from the tray
        self.show()
        self.tray_icon.hide()

    def on_tray_icon_click(self, reason):
        # When the tray icon is double-clicked, restores the window
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.restore_from_tray()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create and show the custom window
    window = CustomWindow()
    window.show()

    sys.exit(app.exec())