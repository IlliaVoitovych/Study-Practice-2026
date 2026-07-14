from core.entity_manager import EntityManager
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.bonus import Bonus


class GameManager:

    def __init__(self, scene):
        self.scene = scene
        self.entities = EntityManager(scene)
        self.score = 0
        self.enemy_spawn_delay = 60
        self.enemy_spawn_timer = 0
        self.bonus_spawn_delay = 540
        self.bonus_spawn_timer = 0
        self.player = Player(scene.WIDTH, scene.HEIGHT)
        self.player.setPos(
            scene.WIDTH / 2 - self.player.WIDTH / 2,
            scene.HEIGHT - 90
        )
        self.entities.add_entity(self.player)

    def spawn_logic(self):
        self.enemy_spawn_timer += 1
        self.bonus_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            self.spawn_enemy()
        if self.bonus_spawn_timer >= self.bonus_spawn_delay:
            self.bonus_spawn_timer = 0
            self.spawn_bonus()

    def tick(self, keys):
        self.player.tick(keys)
        if keys["shoot"] and self.player.can_shoot():
            self.shoot()
        self.entities.tick()
        self.spawn_logic()
        self.check_collisions()
        self.check_bonus_collision()
        # self.update_difficulty()

    def shoot(self):
        bullet = Bullet()
        bullet.setPos(
            self.player.x() + self.player.WIDTH / 2 - bullet.WIDTH / 2,
            self.player.y() - bullet.HEIGHT
        )
        self.entities.add_entity(bullet)
        self.player.reset_cooldown()

    def update_bullets(self):
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active():
                self.scene.removeItem(bullet)
                self.bullets.remove(bullet)

    def spawn_enemy(self):
        enemy = Enemy(self.scene.WIDTH)
        self.entities.add_entity(enemy)

    def spawn_bonus(self):
        bonus = Bonus(self.scene.WIDTH)
        self.entities.add_entity(bonus)

    def update_enemies(self):
        self.enemy_spawn_timer += 1
        if self.enemy_spawn_timer >= self.enemy_spawn_delay:
            self.enemy_spawn_timer = 0
            self.spawn_enemy()
        for enemy in self.enemies[:]:
            enemy.update()
            if not enemy.is_active():
                self.scene.removeItem(enemy)
                self.enemies.remove(enemy)

    def check_collisions(self):
        for bullet in self.entities.bullets:
            for enemy in self.entities.enemies:
                if bullet.collidesWithItem(enemy):
                    bullet.destroy()
                    enemy.destroy()
                    self.score += 10
                    break

    def check_bonus_collision(self):
        for bonus in self.entities.bonuses:
            if self.player.collidesWithItem(bonus):
                bonus.destroy()
                self.score += 50