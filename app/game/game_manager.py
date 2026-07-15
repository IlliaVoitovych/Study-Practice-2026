from core.entity_manager import EntityManager
from core.game_state import GameState
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.bonus import Bonus
from core.record_manager import RecordManager


class GameManager:

    def __init__(self, scene):
        self.scene = scene
        self.entities = EntityManager(scene)
        self.score = 0
        self.record = RecordManager.load_record()
        self.enemy_spawn_delay = 60
        self.enemy_spawn_timer = 0
        self.bonus_spawn_delay = 480
        self.bonus_spawn_timer = 0
        self.double_score = False
        self.double_score_timer = 0
        self.rapid_fire_timer = 0
        self.shield_timer = 0
        self.state = GameState.PLAYING
        self.level = 1
        self.frames = 0
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
            count = 1
            if self.level >= 5:
                count = 2
            if self.level >= 10:
                count = 3
            for _ in range(count):
                self.spawn_enemy()
        if self.bonus_spawn_timer >= self.bonus_spawn_delay:
            self.bonus_spawn_timer = 0
            self.spawn_bonus()

    def tick(self, keys):
        if self.state != GameState.PLAYING:
            return
        self.frames += 1
        self.player.tick(keys)
        if keys["shoot"] and self.player.can_shoot():
            self.shoot()
        self.spawn_logic()
        self.check_collisions()
        self.check_bonus_collision()
        self.check_game_over()
        self.entities.tick()
        self.update_bonus_effects()
        self.update_difficulty()

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
                    points = 10
                    if self.double_score:
                        points *= 2
                    self.score += points
                    break

    def check_bonus_collision(self):
        for bonus in self.entities.bonuses[:]:
            if self.player.collidesWithItem(bonus):
                bonus.effect.apply(self)
                self.last_bonus = bonus.effect.name
                bonus.destroy()

    def update_bonus_effects(self):
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                self.player.SHOOT_COOLDOWN = 15
        if self.double_score_timer > 0:
            self.double_score_timer -= 1
            if self.double_score_timer == 0:
                self.double_score = False
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def update_difficulty(self):
        if self.frames % 900 == 0:
            self.level += 1
            if self.enemy_spawn_delay > 20:
                self.enemy_spawn_delay -= 2
            Enemy.SPEED += 0.4

    def check_game_over(self):
        if self.shield_timer > 0:
            return
        for enemy in self.entities.enemies:
            if self.player.collidesWithItem(enemy):
                self.game_over()
                return
            
    def game_over(self):
        print("GAME OVER")
        self.record = RecordManager.save_record(self.score)
        self.state = GameState.GAME_OVER

    def pause(self):
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume(self):   
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING