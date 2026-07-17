"""
Player Entity Module

Defines the Player class, which represents the player-controlled spaceship.
The player can move left and right, shoot bullets, and collect bonuses.
"""

from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Player(GameObject):
    """
    Represents the player-controlled spaceship.
    
    The player can move horizontally across the bottom of the screen,
    fire bullets at enemies, and collect bonuses. The player is destroyed
    if it collides with an enemy (unless protected by a shield bonus).
    
    Attributes:
        WIDTH (int): Player sprite width in pixels.
        HEIGHT (int): Player sprite height in pixels.
        SPEED (int): Player movement speed in pixels per frame.
        SHOOT_COOLDOWN (int): Frames between shots (modified by Rapid Fire bonus).
    """
    # Player sprite dimensions
    WIDTH = 100
    HEIGHT = 75

    # Player movement speed (pixels per frame)
    SPEED = 6

    # Frames between shots (reduced by Rapid Fire bonus)
    SHOOT_COOLDOWN = 15

    def __init__(self, scene_width, scene_height):
        """
        Initialize a new player spaceship.
        
        Loads the player sprite and initializes the shoot cooldown timer.
        The player is positioned at (0, 0) and should be repositioned by the caller.
        
        Args:
            scene_width (int): Width of the game scene (for boundary checking).
            scene_height (int): Height of the game scene (for boundary checking).
        """
        super().__init__()

        # Load and scale the player sprite
        self.sprite = ResourceManager.load_pixmap("ship.png").scaled(
                self.WIDTH,
                self.HEIGHT,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

        self.scene_width = scene_width
        self.scene_height = scene_height

        # Cooldown timer for shooting (decremented each frame)
        self.cooldown = 0

    def boundingRect(self):
        """
        Get the bounding rectangle for collision detection.
        
        Returns:
            QRectF: Rectangle representing the player's bounds.
        """
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        """
        Render the player spaceship sprite.
        """
        painter.drawPixmap(
        self.boundingRect().toRect(),
        self.sprite
    )

    def tick(self, keys=None):
        """
        Update the player's state each frame.
        
        Handles horizontal movement based on input and decrements the shoot cooldown.
        
        Args:
            keys (dict): Dictionary with keys:
                - "left" (bool): Move player left
                - "right" (bool): Move player right
                Can be None if called without input context.
        """
        # Process movement input
        if keys is not None:
            # Move left
            if keys["left"]:
                self.move_left()

            # Move right
            if keys["right"]:
                self.move_right()

        # Decrement cooldown timer
        if self.cooldown > 0:
            self.cooldown -= 1

    def can_shoot(self):
        """
        Check if the player can shoot.
        
        Returns:
            bool: True if cooldown is expired (can shoot), False otherwise.
        """
        return self.cooldown == 0

    def reset_cooldown(self):
        """
        Reset the shoot cooldown to SHOOT_COOLDOWN value.
        
        Called after firing a shot to prevent rapid uncontrolled firing.
        """
        self.cooldown = self.SHOOT_COOLDOWN

    def move_left(self):
        """
        Move the player left while keeping it within the left boundary.
        
        Doesn't allow moving past the left edge of the screen.
        """
        self.setX(max(0, self.x() - self.SPEED))

    def move_right(self):
        """
        Move the player right while keeping it within the right boundary.
        
        Doesn't allow moving past the right edge of the screen.
        """
        self.setX(
            min(self.scene_width - self.WIDTH,
                self.x() + self.SPEED))