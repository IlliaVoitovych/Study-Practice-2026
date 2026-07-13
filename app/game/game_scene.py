from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from entities.player import Player
from entities.bullet import Bullet
from entities.enemy import Enemy


class GameScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()

        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        self.setBackgroundBrush(QBrush(QColor(10, 10, 30)))

        self.frame = 0
        self.score = 0

        self.player = Player(self.WIDTH, self.HEIGHT)

        self.player.setPos(
            self.WIDTH / 2 - self.player.WIDTH / 2,
            self.HEIGHT - 90
        )

        self.addItem(self.player)

        self.bullets = []
        self.enemies = []
        self.enemy_spawn_delay = 60
        self.enemy_spawn_timer = 0

        self.info = QGraphicsTextItem()
        self.info.setDefaultTextColor(QColor("white"))
        font = self.info.font()
        font.setPointSize(14)
        font.setBold(True)
        self.info.setFont(font)

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

            if not bullet.is_active():
                self.removeItem(bullet)
                self.bullets.remove(bullet)

    def update_scene(self, keys):
        self.frame += 1
        self.player.update(keys)
        if keys["shoot"] and self.player.can_shoot():
            self.shoot()
        self.update_bullets()
        self.update_enemies()
        self.check_collisions()
        self.info.setPlainText(
            f"Frame: {self.frame}\n"
            f"Bullets: {len(self.bullets)}\n"
            f"Enemies: {len(self.enemies)}"
        )
    
    def spawn_enemy(self):
        enemy = Enemy(self.WIDTH)
        self.enemies.append(enemy)
        self.addItem(enemy)

    def update_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            self.spawn_enemy()
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.is_active():
                self.removeItem(enemy)
                self.enemies.remove(enemy)
    
    def check_collisions(self):
        bullets_to_remove = []
        enemies_to_remove = []
        for bullet in self.bullets:
            for enemy in self.enemies:
                if bullet.collidesWithItem(enemy):
                    bullets_to_remove.append(bullet)
                    enemies_to_remove.append(enemy)
                    self.score += 10
                    break

        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.removeItem(bullet)
                self.bullets.remove(bullet)
        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                self.removeItem(enemy)
                self.enemies.remove(enemy)