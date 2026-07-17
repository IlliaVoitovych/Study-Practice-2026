"""
Score Bonus Effect Module

Implements a bonus that awards the player with bonus points.
"""
from effects.bonus_effect import BonusEffect


class ScoreBonus(BonusEffect):
    """
    Bonus effect that awards 100 bonus points.
    
    When collected, the player immediately
    gains 100 points. If the Double Score bonus is active, the points are doubled.
    """

    @property
    def icon(self):
        """
        Get the icon filename for the score bonus.
        
        Returns:
            str: Filename "score.png".
        """
        return "score.png"

    @property
    def name(self):
        """
        Get the display name for the score bonus.
        
        Returns:
            str: "Score".
        """
        return "Score"

    def apply(self, manager):
        """
        Apply the score bonus to the game manager.
        
        Adds 100 points to the player's score. The GameManager handles
        applying the Double Score multiplier if it's active.
        
        Args:
            manager (GameManager): The game manager to add points to.
        """
        manager.score += 100