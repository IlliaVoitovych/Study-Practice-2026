"""
Bonus Entity Module

Defines the Bonus class, which represents power-up bonuses that fall from the top of the screen.
When collected by the player, bonuses apply special effects such as rapid fire, shield, double score.
"""

import random
from core.resource_manager import ResourceManager
from effects.score_bonus import ScoreBonus
from effects.rapid_fire_bonus import RapidFireBonus
from effects.double_score_bonus import DoubleScoreBonus
from effects.shield_bonus import ShieldBonus
from PyQt6.QtCore import QRectF, Qt
from core.game_object import GameObject

# List of all available bonus types
effects = [
    ScoreBonus,
    RapidFireBonus,
    DoubleScoreBonus,
    ShieldBonus
]


class Bonus(GameObject):
    """
    Represents a bonus power-up that falls from the top of the screen.
    
    Bonuses randomly select one of four effects and display an appropriate icon.
    When the player collects a bonus, its effect is applied to the game.
    Bonuses are destroyed if they leave the bottom of the screen without being collected.
    
    Attributes:
        SIZE (int): Bonus sprite size in pixels (bonuses are square).
        SPEED (int): Bonus falling speed in pixels per frame.
        effect: The bonus effect instance that will be applied when collected.
    """

    # Bonus sprite dimensions (square)
    SIZE = 35
    # Bonus falling speed (pixels per frame)
    SPEED = 2

    def __init__(self, scene_width):
        """
        Initialize a new bonus power-up.
        
        Randomly selects a bonus type, positions it at the top of the screen,
        and loads the corresponding sprite.
        
        Args:
            scene_width (int): Width of the game scene (for random positioning).
        """
        super().__init__()

        # Randomly position horizontally at the top of the screen
        x = random.randint(0, scene_width - self.SIZE)
        self.setPos(x, -self.SIZE)

        # Randomly select a bonus effect
        self.effect = random.choice(effects)()

        # Load and scale the sprite for the selected bonus type
        self.sprite = ResourceManager.load_pixmap(
            self.effect.icon).scaled(
            self.SIZE,
            self.SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def boundingRect(self):
        """
        Get the bounding rectangle for collision detection.
        
        Returns:
            QRectF: Square rectangle representing the bonus's bounds.
        """
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        """
        Render the bonus sprite.
        """
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):
        """
        Update the bonus's position each frame.
        
        Moves the bonus downward. If the bonus leaves the bottom of the screen,
        it is marked for destruction (uncollected bonus disappears).
        """
        # Move downward
        self.setY(
            self.y() + self.SPEED
        )

        # Destroy if off-screen (bottom)
        if self.y() > 650:
            self.destroy()