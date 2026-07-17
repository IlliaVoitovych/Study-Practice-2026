"""
Shield Bonus Effect Module

Implements a bonus that provides temporary protection from collisions.
"""
from effects.bonus_effect import BonusEffect


class ShieldBonus(BonusEffect):
    """
    Bonus effect that provides temporary collision protection.
    
    When collected, the player becomes protected from asteroid collisions.
    If the shield is active, colliding with an asteroid will not end the game.
    The shield lasts for 600 frames (approximately 10 seconds).
    """

    @property
    def icon(self):
        """
        Get the icon filename for the shield bonus.
        
        Returns:
            str: Filename "shield.png".
        """
        return "shield.png"

    @property
    def name(self):
        """
        Get the display name for the shield bonus.
        
        Returns:
            str: "Shield".
        """
        return "Shield"

    def apply(self, manager):
        """
        Apply the shield bonus to the game manager.
        
        Sets the shield_timer to 600 frames. While this timer is active,
        the player cannot collide with asteroids and die. When the timer
        expires, the shield protection is removed.
        
        Args:
            manager (GameManager): The game manager to apply the shield to.
        """
        manager.shield_timer = 600