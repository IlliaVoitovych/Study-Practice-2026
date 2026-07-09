from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout


class GameWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Space Shooter")
        self.setFixedSize(800, 600)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Game Window"))

        self.setLayout(layout)