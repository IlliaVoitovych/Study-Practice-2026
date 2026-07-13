from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from entities.player import Player
from entities.bullet import Bullet


class GameScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        self.setBackgroundBrush(QBrush(QColor(10, 10, 30)))

        self.frame = 0

        self.player = Player(self.WIDTH, self.HEIGHT)

        self.player.setPos(
            self.WIDTH / 2 - self.player.WIDTH / 2,
            self.HEIGHT - 90
        )

        self.addItem(self.player)

        self.bullets = []

        self.info = QGraphicsTextItem()
        self.info.setDefaultTextColor(QColor("white"))
        self.info.setPos(10, 10)

        self.addItem(self.info)

    def shoot(self):

        bullet = Bullet()

        bullet.setPos(
            self.player.x() + self.player.WIDTH / 2 - bullet.WIDTH / 2,
            self.player.y() - bullet.HEIGHT
        )

        self.addItem(bullet)

        self.bullets.append(bullet)

        self.player.reset_cooldown()

    def update_bullets(self):

        for bullet in self.bullets[:]:

            bullet.update()

            if not bullet.active:
                self.removeItem(bullet)
                self.bullets.remove(bullet)

    def update_scene(self, keys):

        self.frame += 1

        self.player.update(keys)

        if keys["shoot"] and self.player.can_shoot():
            self.shoot()

        self.update_bullets()

        self.info.setPlainText(
            f"Frame: {self.frame}\n"
            f"Bullets: {len(self.bullets)}"
        )