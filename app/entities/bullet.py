from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen

from core.game_object import GameObject


class Bullet(GameObject):

    WIDTH = 6
    HEIGHT = 20
    SPEED = 10

    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor("yellow")))
        painter.setPen(QPen(QColor("white"), 1))
        painter.drawRect(0, 0, self.WIDTH, self.HEIGHT)

    def update(self):
        self.setY(self.y() - self.SPEED)

        if self.y() + self.HEIGHT < 0:
            self.destroy()