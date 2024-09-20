import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QSystemTrayIcon, QMenu
from PyQt6.QtGui import QPainter, QColor, QBrush, QIcon, QAction  # Corrigido: QAction agora está em PyQt6.QtGui
from PyQt6.QtCore import Qt, QRect, QSize, QPoint
import os

class CustomWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurações da janela
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)  # Sem barra de título e não aparece na taskbar
        self.setFixedSize(240, 500)  # Tamanho fixo
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)  # Fundo transparente

        # Definindo a cor de fundo com 80% de opacidade
        self.background_color = QColor(0, 0, 0, 204)  # Preto com 80% de opacidade (204/255)

        # Layout básico para adicionar os botões
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Botão de fechar (vermelho)
        self.close_button = QPushButton(self)
        self.close_button.setFixedSize(20, 20)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: red;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: lightcoral;
            }
        """)
        self.close_button.clicked.connect(self.close)

        # Botão de minimizar (azul)
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

        # Posicionamento dos botões
        self.close_button.move(210, 10)  # Posição no canto superior direito
        self.minimize_button.move(180, 10)  # Posição ao lado esquerdo do botão de fechar

        # Evento de clique para maximizar
        self.clicked = False  # Flag para controlar o estado de maximização
        self.old_geometry = self.geometry()

        # Variáveis para arrastar e soltar
        self.dragging = False  # Controle do estado de arraste
        self.drag_position = QPoint(0, 0)  # Posição inicial do mouse ao arrastar

        # System Tray Icon - usar o ícone personalizado (gota verde)
        self.tray_icon = QSystemTrayIcon(self)

        # Define o caminho absoluto para o ícone
        icon_path = os.path.join(os.path.dirname(__file__), "Bin/icon.png")
        
        if os.path.exists(icon_path):
            self.tray_icon.setIcon(QIcon(icon_path))  # Carregar o ícone corretamente
        else:
            print(f"Ícone não encontrado no caminho: {icon_path}")
            self.tray_icon.setIcon(QIcon())  # Usa um ícone vazio se o ícone não for encontrado

        # Criação do menu do tray icon
        tray_menu = QMenu()

        # Ação para restaurar a janela a partir do tray
        restore_action = QAction("Show", self)
        restore_action.triggered.connect(self.restore_from_tray)
        tray_menu.addAction(restore_action)

        # Ação para sair da aplicação a partir do tray
        exit_action = QAction("Close", self)
        exit_action.triggered.connect(self.close)
        tray_menu.addAction(exit_action)

        # Conectar o menu ao tray icon
        self.tray_icon.setContextMenu(tray_menu)

        # Conectar o double click para restaurar a janela
        self.tray_icon.activated.connect(self.on_tray_icon_click)

    def paintEvent(self, event):
        # Pintar o fundo arredondado da janela
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        rect = QRect(0, 0, self.width(), self.height())
        painter.setBrush(QBrush(self.background_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(rect, 15, 15)  # Cantos arredondados

    def mousePressEvent(self, event):
        # Iniciar o arrasto ao pressionar o botão esquerdo do mouse
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        # Atualiza a posição da janela conforme o mouse é movido
        if self.dragging:
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()

    def mouseReleaseEvent(self, event):
        # Finaliza o arrasto quando o botão do mouse é solto
        self.dragging = False

    def minimize_to_tray(self):
        # Minimiza a janela e esconde-a, mostrando o ícone no tray
        self.hide()
        self.tray_icon.show()

    def restore_from_tray(self):
        # Restaura a janela a partir do tray
        self.show()
        self.tray_icon.hide()

    def on_tray_icon_click(self, reason):
        # Quando o ícone do tray é clicado duas vezes, restaura a janela
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.restore_from_tray()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Criar e mostrar a janela personalizada
    window = CustomWindow()
    window.show()

    sys.exit(app.exec())