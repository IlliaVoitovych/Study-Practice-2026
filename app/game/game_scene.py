from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from entities.player import Player


class GameScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.setSceneRect(
            0,
            0,
            self.WIDTH,
            self.HEIGHT
        )

        self.setBackgroundBrush(
            QBrush(QColor(10, 10, 30))
        )

        self.frame = 0

        self.player = Player()

        self.player.setPos(
            self.WIDTH / 2 - 25,
            self.HEIGHT - 90
        )

        self.addItem(self.player)

        self.info = QGraphicsTextItem()

        self.info.setDefaultTextColor(
            QColor("white")
        )

        self.info.setPos(10, 10)

        self.addItem(self.info)

    def update_scene(self):
        self.frame += 1

        self.info.setPlainText(
            f"Frame: {self.frame}"
        )