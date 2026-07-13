from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem


class Player(QGraphicsItem):
    WIDTH = 50
    HEIGHT = 60
    SPEED = 6

    def __init__(self):
        super().__init__()

    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.WIDTH,
            self.HEIGHT
        )

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor(0, 220, 255)))
        painter.setPen(QPen(QColor("white"), 2))

        painter.drawRoundedRect(
            0,
            0,
            self.WIDTH,
            self.HEIGHT,
            8,
            8
        )

    def move_left(self):
        self.setX(self.x() - self.SPEED)

    def move_right(self):
        self.setX(self.x() + self.SPEED)

    def move_up(self):
        self.setY(self.y() - self.SPEED)

    def move_down(self):
        self.setY(self.y() + self.SPEED)