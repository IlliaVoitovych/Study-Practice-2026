from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
)

from game.game_window import GameWindow


class MainMenu(QWidget):
    def __init__(self):
        super().__init__()

        self.game_window = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Space Shooter")
        self.setFixedSize(900, 700)

        self.setStyleSheet("""
            QWidget{
                background-color:#101820;
            }

            QLabel{
                color:white;
                font-size:34px;
                font-weight:bold;
            }

            QPushButton{
                background:#2E86DE;
                color:white;
                font-size:18px;
                border-radius:8px;
                min-height:45px;
            }

            QPushButton:hover{
                background:#54A0FF;
            }
        """)

        title = QLabel("SPACE SHOOTER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Старт")
        exit_button = QPushButton("Вихід")

        start_button.clicked.connect(self.start_game)
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()

        layout.addStretch()

        layout.addWidget(title)

        layout.addSpacing(40)

        layout.addWidget(start_button)

        layout.addWidget(exit_button)

        layout.addStretch()

        layout.setContentsMargins(200, 60, 200, 60)

        self.setLayout(layout)

    def start_game(self):
        self.game_window = GameWindow()
        self.game_window.show()

        self.close()