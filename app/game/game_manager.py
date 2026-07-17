"""
Game Manager Module

The central controller for game logic. Manages all game entities, handles collision
detection, spawning logic, difficulty progression, bonus effects, and game state.
"""

from core.entity_manager import EntityManager
from core.game_state import GameState
from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.bonus import Bonus
from core.record_manager import RecordManager


class GameManager:
    """
    Central game controller managing all game logic and entity interactions.
    
    Responsibilities:
    - Managing all game entities through EntityManager
    - Spawning enemies and bonuses at controlled intervals
    - Detecting collisions between bullets, enemies, bonuses, and player
    - Applying bonus effects and managing their timers
    - Tracking score, level, and difficulty progression
    - Managing game state transitions (PLAYING, PAUSED, GAME_OVER)
    
    Attributes:
        scene: The game scene containing all rendered entities
        entities: EntityManager handling entity collections
        score: Current player score
        record: Highest score achieved
        state: Current game state (PLAYING, PAUSED, or GAME_OVER)
        level: Current difficulty level (1+)
    """

    def __init__(self, scene):
        """
        Initialize the game manager.
        
        Sets up the entity manager, initializes the player, loads the high score,
        and prepares spawning and difficulty parameters.
        
        Args:
            scene (GameScene): The game scene to manage.
        """
        self.scene = scene
        self.entities = EntityManager(scene)
        self.score = 0
        self.record = RecordManager.load_record()
        self.enemy_spawn_delay = 60  # Frames between enemy spawns (decreases with difficulty)
        self.enemy_spawn_timer = 0   # Counter to trigger spawning
        self.bonus_spawn_delay = 480  # Frames between bonus spawns
        self.bonus_spawn_timer = 0    # Counter to trigger spawning
        self.double_score = False          # Flag for double score bonus
        self.double_score_timer = 0        # Frames remaining for double score
        self.rapid_fire_timer = 0          # Frames remaining for rapid fire
        self.shield_timer = 0              # Frames remaining for shield protection
        self.state = GameState.PLAYING  # Current game state
        self.level = 1                   # Difficulty level (increases over time)
        self.frames = 0                  # Total frames elapsed
        
        # Initialize player and add to scene
        self.player = Player(scene.WIDTH, scene.HEIGHT)
        self.player.setPos(
            scene.WIDTH / 2 - self.player.WIDTH / 2,
            scene.HEIGHT - 90
        )
        self.entities.add_entity(self.player)

    def spawn_logic(self):
        """
        Handle spawn timing for enemies and bonuses.
        
        Increments spawn timers and spawns entities when timers expire.
        Difficulty increases the number of simultaneous enemies at higher levels.
        
        Difficulty scaling:
        - Level 1-4: 1 enemy per spawn
        - Level 5-9: 2 enemies per spawn
        - Level 10+: 3 enemies per spawn
        """
        # Update enemy spawn timer
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
        """
        Main game update called every frame.
        
        Only updates game logic when in PLAYING state. Orchestrates all game updates:
        1. Update player movement
        2. Handle shooting
        3. Spawn enemies and bonuses
        4. Check all collisions
        5. Update all entities
        6. Update bonus effect timers
        7. Increase difficulty
        
        Args:
            keys (dict): Current key states:
                - "left" (bool): A key
                - "right" (bool): D key
                - "shoot" (bool): Space bar
        """
        # Only update if game is actively playing
        if self.state != GameState.PLAYING:
            return

        # Increment frame counter
        self.frames += 1

        # Update player position based on input
        self.player.tick(keys)

        # Fire bullet if spacebar pressed and ready
        if keys["shoot"] and self.player.can_shoot():
            self.shoot()

        # Spawn new enemies and bonuses
        self.spawn_logic()

        # Check all collision types
        self.check_collisions()           # Bullet-enemy collisions
        self.check_bonus_collision()      # Player-bonus collisions
        self.check_game_over()            # Enemy-player collisions

        # Update all entities (movement, animation, etc.)
        self.entities.tick()

        # Manage bonus effect timers
        self.update_bonus_effects()

        # Increase difficulty as game progresses
        self.update_difficulty()

    def shoot(self):
        """
        Fire a bullet from the player's current position.
        
        Creates a bullet at the player's center and slightly above the player,
        adds it to the entity manager, and resets the shooting cooldown.
        """
        # Create new bullet
        bullet = Bullet()
        # Position at player's center, above the sprite
        bullet.setPos(
            self.player.x() + self.player.WIDTH / 2 - bullet.WIDTH / 2,
            self.player.y() - bullet.HEIGHT
        )
        # Add to scene and entity collections
        self.entities.add_entity(bullet)
        # Start cooldown to prevent rapid firing
        self.player.reset_cooldown()

    def update_bullets(self):
        """
        Method for updating bullets.
        """
        for bullet in self.bullets[:]:
            bullet.update()
            if not bullet.is_active():
                self.scene.removeItem(bullet)
                self.bullets.remove(bullet)

    def spawn_enemy(self):
        """
        Create and spawn a new enemy at the top of the screen.
        
        Randomly positions the enemy horizontally and adds it to the entity manager.
        """
        enemy = Enemy(self.scene.WIDTH)
        self.entities.add_entity(enemy)

    def spawn_bonus(self):
        """
        Create and spawn a new bonus at the top of the screen.
        
        Randomly selects a bonus type and positions it horizontally at the top.
        """
        bonus = Bonus(self.scene.WIDTH)
        self.entities.add_entity(bonus)

    def update_enemies(self):
        """
        Method for updating enemies.
        """
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
        """
        Detect and handle bullet-enemy collisions.
        
        For each bullet-enemy pair that collides:
        1. Destroy both the bullet and enemy
        2. Award 10 points (20 if Double Score is active)
        3. Continue checking other collisions
        """
        for bullet in self.entities.bullets:
            for enemy in self.entities.enemies:
                # Check if bullet and enemy overlap
                if bullet.collidesWithItem(enemy):
                    # Remove both from game
                    bullet.destroy()
                    enemy.destroy()
                    # Award points
                    points = 10
                    if self.double_score:
                        points *= 2  # Double points if bonus active
                    self.score += points
                    break

    def check_bonus_collision(self):
        """
        Detect and handle player-bonus collisions.
        
        When player collects a bonus:
        1. Apply the bonus effect to the game manager
        2. Record the bonus name for display
        3. Destroy the bonus
        """
        for bonus in self.entities.bonuses[:]:
            # Check if player and bonus overlap
            if self.player.collidesWithItem(bonus):
                # Apply the bonus effect (modifies game state)
                bonus.effect.apply(self)
                # Track which bonus was collected (for debugging)
                self.last_bonus = bonus.effect.name
                # Remove bonus from game
                bonus.destroy()

    def update_bonus_effects(self):
        """
        Update all active bonus effect timers.
        
        Decrements timers for:
        - Rapid Fire: Resets SHOOT_COOLDOWN to normal when expired
        - Double Score: Disables double score flag when expired
        - Shield: Decrements but doesn't need special handling on expiry
        """
        # Handle Rapid Fire bonus expiration
        if self.rapid_fire_timer > 0:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer == 0:
                # Restore normal shooting speed
                self.player.SHOOT_COOLDOWN = 15

        # Handle Double Score bonus expiration
        if self.double_score_timer > 0:
            self.double_score_timer -= 1
            if self.double_score_timer == 0:
                # Disable double score
                self.double_score = False

        # Handle Shield bonus duration (just decrement timer)
        if self.shield_timer > 0:
            self.shield_timer -= 1

    def update_difficulty(self):
        """
        Increase difficulty every 900 frames (15 seconds at 60 FPS).
        
        Increases level and modifies spawn rates and enemy speed:
        - Level increases
        - Enemy spawn rate increases (spawn_delay decreases until minimum)
        - Enemy speed increases
        """
        # Check every 900 frames (15 seconds)
        if self.frames % 900 == 0:
            # Increase difficulty level
            self.level += 1
            # Speed up enemy spawning (but not below 20 frame minimum)
            if self.enemy_spawn_delay > 20:
                self.enemy_spawn_delay -= 2
            # Increase enemy movement speed
            Enemy.SPEED += 0.4

    def check_game_over(self):
        """
        Detect player-enemy collisions and trigger game over.
        
        If shield is active, ignore collisions (shield protects from one hit).
        Otherwise, check if player overlaps with any enemy and end the game.
        """
        # Shield protects from collisions
        if self.shield_timer > 0:
            return

        # Check each enemy for collision with player
        for enemy in self.entities.enemies:
            if self.player.collidesWithItem(enemy):
                # Collision detected - end game
                self.game_over()
                return

    def game_over(self):
        """
        Handle game over state.
        
        1. Saves the score if it's a new record
        2. Changes game state to GAME_OVER (stops all updates)
        """
        print("GAME OVER")
        # Save the score and update record if needed
        self.record = RecordManager.save_record(self.score)
        # Change state to prevent further game updates
        self.state = GameState.GAME_OVER

    def pause(self):
        """
        Pause the game.
        
        Changes game state to PAUSED, which prevents game logic updates
        but allows the pause menu to be displayed. The game loop continues
        running to allow input processing.
        """
        if self.state == GameState.PLAYING:
            self.state = GameState.PAUSED

    def resume(self):
        """
        Resume the game from pause.
        
        Changes game state back to PLAYING, allowing game logic updates
        and gameplay to continue.
        """
        if self.state == GameState.PAUSED:
            self.state = GameState.PLAYING