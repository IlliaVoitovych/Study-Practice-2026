"""
Base GameObject Class

This module defines the GameObject base class, which is the foundation for all
interactive entities in the Space Shooter game (player, enemies, bullets, bonuses).

All game objects inherit from both QGraphicsItem and this class.
"""

from PyQt6.QtWidgets import QGraphicsItem


class GameObject(QGraphicsItem):
    """
    Base class for all game objects in the Space Shooter.
    
    Provides common lifecycle management for all entities including:
    - Active state tracking
    - Destruction handling
    - Tick/update mechanism
    
    Inherits from QGraphicsItem to enable rendering in the game scene.
    """

    def __init__(self):
        """
        Initialize a new GameObject.
        
        Sets the initial active state to True (object is alive and active).
        """
        super().__init__()
        self.active = True

    def destroy(self):
        """
        Mark this game object as destroyed/inactive.
        
        This sets the active flag to False. The EntityManager will remove
        the object from the scene and its collections during the next tick.
        """
        self.active = False

    def is_active(self):
        """
        Check if this game object is currently active.
        
        Returns:
            bool: True if object is active, False if destroyed.
        """
        return self.active

    def tick(self, *args, **kwargs):
        """
        Update the game object's state for this frame.
        
        This method is called every frame by the EntityManager and should be
        overridden in subclasses to implement entity-specific behavior such as:
        - Movement
        - Animation
        - Collision checks
        - Other game logic
        """
        pass