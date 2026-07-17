"""
Enemy Entity Module

Defines the Enemy class, which represents asteroids that fall from the top of the screen.
Enemies move downward at a constant speed and must be destroyed by the player's bullets.
"""

import random

from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Enemy(GameObject):
    """
    Represents an enemy asteroid falling from the top of the screen.
    
    Enemies fall downward at a constant speed and vary in appearance by randomly
    selecting from multiple asteroid sprite variations. Destroying enemies awards
    points to the player. Enemies are destroyed if they leave the bottom of the screen.
    
    Attributes:
        SIZE (int): Enemy sprite size in pixels (asteroids are square).
        SPEED (int): Enemy movement speed in pixels per frame.
    """

    # Enemy sprite dimensions (square)
    SIZE = 45
    # Enemy movement speed (pixels per frame, increased with difficulty)
    SPEED = 3

    def __init__(self, scene_width):
        """
        Initialize a new enemy asteroid.
        
        Randomly positions the enemy at the top of the screen and selects
        a random asteroid sprite variation.
        
        Args:
            scene_width (int): Width of the game scene (for random positioning).
        """
        super().__init__()
        
        self.scene_width = scene_width

        # Randomly position horizontally at the top of the screen
        x = random.randint(0, scene_width - self.SIZE)
        self.setPos(x, -self.SIZE)

        # Randomly select an asteroid sprite variation
        sprites = [
            "asteroid1.png",
            "asteroid2.png",
            "asteroid3.png",
            "asteroid4.png",
        ]
        self.sprite = ResourceManager.load_pixmap(
            random.choice(sprites)
        ).scaled(
            self.SIZE,
            self.SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def boundingRect(self):
        """
        Get the bounding rectangle for collision detection.
        
        Returns:
            QRectF: Square rectangle representing the enemy's bounds.
        """
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        """
        Render the enemy asteroid sprite.
        """
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):
        """
        Update the enemy's position each frame.
        
        Moves the enemy downward. If the enemy leaves the bottom of the screen,
        it is marked for destruction (this counts as a player survival if not hit).
        """
        # Move downward
        self.setY(self.y() + self.SPEED)

        # Destroy if off-screen (bottom)
        if self.y() > 650:
            self.destroy()