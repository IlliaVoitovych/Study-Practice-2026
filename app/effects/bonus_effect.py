"""
Bonus Effect Base Class Module

Defines the abstract base class for all bonus power-up effects in the game.
All specific bonus types (score, rapid fire, shield, ...) inherit from this class.
"""

from abc import ABC, abstractmethod


class BonusEffect(ABC):
    """
    Abstract base class for all bonus power-up effects.
    
    Each bonus type must implement:
    - icon property: Path to the bonus sprite image
    - name property: Display name of the bonus
    - apply method: Logic to apply the bonus effect to the game
    
    This abstract interface ensures consistency across all bonus types and
    makes it easy to add new bonus types in the future.
    """

    @property
    @abstractmethod
    def icon(self):
        """
        Get the icon file path for this bonus.
        
        Returns:
            str: Filename of the bonus sprite image (e.g., "shield.png").
                 Should be located in the assets directory.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Get the display name of this bonus.
        
        Returns:
            str: Human-readable name of the bonus (e.g., "Shield", "Rapid Fire").
                 Displayed in debug info and can be used for UI.
        """
        pass

    @abstractmethod
    def apply(self, manager):
        """
        Apply this bonus effect to the game.
        
        This method is called when the player collects this bonus and should
        implement all the logic for activating the bonus, such as:
        - Modifying game state (scores, timers, flags)
        - Applying effects to the player
        - Triggering any visual/audio feedback
        
        Args:
            manager (GameManager): The game manager instance to modify game state.
        """
        pass