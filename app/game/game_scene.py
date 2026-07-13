from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from game.game_manager import GameManager


class GameScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        self.setBackgroundBrush(QBrush(QColor(10, 10, 30)))

        self.frame = 0
        self.score = 0

        self.manager = GameManager(self)

        self.info = QGraphicsTextItem()
        self.info.setDefaultTextColor(QColor("white"))
        font = self.info.font()
        font.setPointSize(14)
        font.setBold(True)
        self.info.setFont(font)

        self.addItem(self.info)

    def update_scene(self, keys):
        self.frame += 1
        self.manager.tick(keys)
        self.info.setPlainText(
            f"Score : {self.manager.score}\n"
            f"Enemies : {len(self.manager.entities.enemies)}\n"
            f"Bullets : {len(self.manager.entities.bullets)}"
        )