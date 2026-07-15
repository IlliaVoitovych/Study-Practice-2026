from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Player(GameObject):
    # orig 50x60
    WIDTH = 100
    HEIGHT = 75

    SPEED = 6

    SHOOT_COOLDOWN = 15

    def __init__(self, scene_width, scene_height):
        super().__init__()

        self.sprite = ResourceManager.load_pixmap("ship.png").scaled(
                self.WIDTH,
                self.HEIGHT,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.scene_width = scene_width
        self.scene_height = scene_height

        self.cooldown = 0

    def boundingRect(self):
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(
        self.boundingRect().toRect(),
        self.sprite
    )

    def tick(self, keys=None):

        if keys is not None:

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
        self.setX(
            min(self.scene_width - self.WIDTH,
                self.x() + self.SPEED)
        )

    def move_up(self):
        self.setY(max(0, self.y() - self.SPEED))

    def move_down(self):
        self.setY(
            min(self.scene_height - self.HEIGHT,
                self.y() + self.SPEED)
        )