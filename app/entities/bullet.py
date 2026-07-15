from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Bullet(GameObject):

    WIDTH = 6
    HEIGHT = 20
    SPEED = 10

    def __init__(self):
        super().__init__()
        self.sprite = ResourceManager.load_pixmap(
            "bullet.png"
    ).scaled(
        self.WIDTH,
        self.HEIGHT,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    def boundingRect(self):
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):
        self.setY(self.y() - self.SPEED)

        if self.y() + self.HEIGHT < 0:
            self.destroy()