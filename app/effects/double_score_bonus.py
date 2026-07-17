"""
Double Score Bonus Effect Module

Implements a bonus that temporarily doubles all points earned.
"""

from effects.bonus_effect import BonusEffect


class DoubleScoreBonus(BonusEffect):
    """
    Bonus effect that temporarily doubles all points earned.
    
    When collected, all points earned from destroying enemies are doubled.
    This includes the normal 10 points per asteroid and any bonus points
    from the Score bonus. The effect lasts for 600 frames (approximately 10 seconds).
    """

    @property
    def icon(self):
        """
        Get the icon filename for the double score bonus.
        
        Returns:
            str: Filename "double_score.png".
        """
        return "double_score.png"

    @property
    def name(self):
        """
        Get the display name for the double score bonus.
        
        Returns:
            str: "Double Score".
        """
        return "Double Score"

    def apply(self, manager):
        """
        Apply the double score bonus to the game manager.
        
        Sets the double_score flag to True and starts the double_score_timer.
        When the timer expires, the flag is reset to False.
        
        Args:
            manager (GameManager): The game manager to apply double score to.
        """
        manager.double_score = True
        manager.double_score_timer = 600