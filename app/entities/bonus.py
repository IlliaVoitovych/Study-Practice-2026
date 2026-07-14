import random
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from core.game_object import GameObject


class Bonus(GameObject):

    SIZE = 25
    SPEED = 2

    def __init__(self, scene_width):
        super().__init__()

        x = random.randint(0, scene_width - self.SIZE)

        self.setPos(x, -self.SIZE)

    def boundingRect(self):
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("green")))
        painter.setPen(QPen(QColor("white"), 2))

        painter.drawEllipse(
            0,
            0,
            self.SIZE,
            self.SIZE
        )

    def tick(self):

        self.setY(
            self.y() + self.SPEED
        )

        if self.y() > 650:
            self.destroy()