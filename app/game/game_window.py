from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsView,
    QVBoxLayout,
)

from game.game_scene import GameScene


class GameWindow(QWidget):
    WIDTH = 800
    HEIGHT = 600

    FPS = 60

    def __init__(self):
        super().__init__()

        self.scene = GameScene()

        # Стан клавіш
        self.keys = {
            Qt.Key.Key_Left: False,
            Qt.Key.Key_Right: False,
            Qt.Key.Key_Up: False,
            Qt.Key.Key_Down: False,
            Qt.Key.Key_A: False,
            Qt.Key.Key_D: False,
            Qt.Key.Key_W: False,
            Qt.Key.Key_S: False,
            Qt.Key.Key_Space: False,
        }

        self.init_ui()
        self.init_game_loop()

    def init_ui(self):
        self.setWindowTitle("Space Shooter")
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        self.view = QGraphicsView(self.scene)

        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)

        layout = QVBoxLayout()

        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self.setLayout(layout)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_game_loop(self):
        self.timer = QTimer()

        self.timer.timeout.connect(self.game_loop)

        interval = int(1000 / self.FPS)

        self.timer.start(interval)

    def game_loop(self):

        if self.keys[Qt.Key.Key_Left] or self.keys[Qt.Key.Key_A]:
            self.scene.player.move_left()

        if self.keys[Qt.Key.Key_Right] or self.keys[Qt.Key.Key_D]:
            self.scene.player.move_right()

        if self.keys[Qt.Key.Key_Up] or self.keys[Qt.Key.Key_W]:
            self.scene.player.move_up()

        if self.keys[Qt.Key.Key_Down] or self.keys[Qt.Key.Key_S]:
            self.scene.player.move_down()

        self.scene.update_scene()

    def keyPressEvent(self, event):
        key = event.key()

        if key in self.keys:
            self.keys[key] = True

    def keyReleaseEvent(self, event):
        key = event.key()

        if key in self.keys:
            self.keys[key] = False