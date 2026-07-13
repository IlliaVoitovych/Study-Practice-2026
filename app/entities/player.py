from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem


class Player(QGraphicsItem):
    WIDTH = 50
    HEIGHT = 60
    SPEED = 6

    def __init__(self, scene_width, scene_height):
        super().__init__()

        self.scene_width = scene_width
        self.scene_height = scene_height

    def boundingRect(self):
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(QColor(0, 220, 255)))
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawRoundedRect(0, 0, self.WIDTH, self.HEIGHT, 8, 8)

    def update(self, keys):
        """Оновлення стану гравця."""

        if keys["left"]:
            self.move_left()

        if keys["right"]:
            self.move_right()

        if keys["up"]:
            self.move_up()

        if keys["down"]:
            self.move_down()

    def move_left(self):
        if self.x() > 0:
            self.setX(max(0, self.x() - self.SPEED))

    def move_right(self):
        if self.x() < self.scene_width - self.WIDTH:
            self.setX(min(self.scene_width - self.WIDTH,
                          self.x() + self.SPEED))

    def move_up(self):
        if self.y() > 0:
            self.setY(max(0, self.y() - self.SPEED))

    def move_down(self):
        if self.y() < self.scene_height - self.HEIGHT:
            self.setY(min(self.scene_height - self.HEIGHT,
                          self.y() + self.SPEED))