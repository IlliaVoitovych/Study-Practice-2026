from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from PyQt6.QtWidgets import QGraphicsItem


class Player(QGraphicsItem):

    WIDTH = 50
    HEIGHT = 60

    SPEED = 6

    SHOOT_COOLDOWN = 15

    def __init__(self, scene_width, scene_height):
        super().__init__()

        self.scene_width = scene_width
        self.scene_height = scene_height

        self.cooldown = 0

    def boundingRect(self):
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

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

    def update(self, keys):

        if keys["left"]:
            self.move_left()

        if keys["right"]:
            self.move_right()

        if keys["up"]:
            self.move_up()

        if keys["down"]:
            self.move_down()

        if self.cooldown > 0:
            self.cooldown -= 1

    def can_shoot(self):
        return self.cooldown == 0

    def reset_cooldown(self):
        self.cooldown = self.SHOOT_COOLDOWN

    def move_left(self):
        self.setX(max(0, self.x() - self.SPEED))

    def move_right(self):
        self.setX(min(self.scene_width - self.WIDTH,
                      self.x() + self.SPEED))

    def move_up(self):
        self.setY(max(0, self.y() - self.SPEED))

    def move_down(self):
        self.setY(min(self.scene_height - self.HEIGHT,
                      self.y() + self.SPEED))