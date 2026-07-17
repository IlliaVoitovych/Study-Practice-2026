"""
Bullet Entity Module

Defines the Bullet class, which represents projectiles fired by the player.
Bullets move upward and are destroyed when they leave the top of the screen.
"""

from PyQt6.QtCore import QRectF, Qt
from core.resource_manager import ResourceManager
from core.game_object import GameObject


class Bullet(GameObject):
    """
    Represents a bullet projectile fired by the player.
    
    Bullets travel upward at a constant speed and are destroyed when they
    leave the top of the screen. Used for collision detection against enemies.
    
    Attributes:
        WIDTH (int): Bullet sprite width in pixels.
        HEIGHT (int): Bullet sprite height in pixels.
        SPEED (int): Bullet movement speed in pixels per frame.
    """

    # Bullet dimensions
    WIDTH = 6
    HEIGHT = 20
    # Bullet movement speed (pixels per frame)
    SPEED = 10

    def __init__(self):
        """
        Initialize a new bullet.
        
        Loads the bullet sprite from assets and scales it to the appropriate size.
        The bullet is positioned at (0, 0) and should be repositioned by the caller.
        """
        super().__init__()
        # Load and scale the bullet sprite
        self.sprite = ResourceManager.load_pixmap(
            "bullet.png"
        ).scaled(
            self.WIDTH,
            self.HEIGHT,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def boundingRect(self):
        """
        Get the bounding rectangle for collision detection.
        
        Returns:
            QRectF: Rectangle representing the bullet's bounds.
        """
        return QRectF(0, 0, self.WIDTH, self.HEIGHT)

    def paint(self, painter, option, widget=None):
        """
        Render the bullet sprite.
        """
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):
        """
        Update the bullet's position each frame.
        
        Moves the bullet upward. If the bullet leaves the top of the screen,
        it is marked for destruction.
        """
        # Move upward
        self.setY(self.y() - self.SPEED)

        # Destroy if off-screen (top)
        if self.y() + self.HEIGHT < 0:
            self.destroy()