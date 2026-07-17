"""
Rapid Fire Bonus Effect Module

Implements a bonus that temporarily increases the player's firing rate.
"""
from effects.bonus_effect import BonusEffect


class RapidFireBonus(BonusEffect):
    """
    Bonus effect that temporarily enables rapid fire mode.
    
    When collected, the player's shooting cooldown is reduced from 15 frames
    to 5 frames, allowing much faster shooting. The effect lasts for 600 frames
    (approximately 10 seconds at 60 FPS).
    """

    @property
    def icon(self):
        """
        Get the icon filename for the rapid fire bonus.
        
        Returns:
            str: Filename "rapid_fire.png".
        """
        return "rapid_fire.png"

    @property
    def name(self):
        """
        Get the display name for the rapid fire bonus.
        
        Returns:
            str: "Rapid Fire".
        """
        return "Rapid Fire"

    def apply(self, manager):
        """
        Apply the rapid fire bonus to the game manager.
        
        Sets the player's shooting cooldown to 5 frames (faster than normal 15)
        and starts the rapid fire timer for 600 frames. When the timer expires,
        the cooldown is reset to normal.
        
        Args:
            manager (GameManager): The game manager to apply rapid fire to.
        """
        manager.player.SHOOT_COOLDOWN = 5
        manager.rapid_fire_timer = 600