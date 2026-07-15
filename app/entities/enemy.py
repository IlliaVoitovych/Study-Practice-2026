import random

from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Enemy(GameObject):

    SIZE = 45
    SPEED = 3

    def __init__(self, scene_width):
        super().__init__()

        self.scene_width = scene_width

        x = random.randint(0, scene_width - self.SIZE)

        self.setPos(x, -self.SIZE)

        sprites = ["asteroid1.png", "asteroid2.png", "asteroid3.png", "asteroid4.png",]
        self.sprite = ResourceManager.load_pixmap(
            random.choice(sprites)
        ).scaled(
            self.SIZE,
            self.SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def boundingRect(self):
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):
        self.setY(self.y() + self.SPEED)

        if self.y() > 650:
            self.destroy()