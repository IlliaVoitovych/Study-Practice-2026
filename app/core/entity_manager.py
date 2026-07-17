"""
Entity Manager Module

This module provides the central management system for all game entities.
It handles adding, removing, and updating all game objects (player, enemies, bullets, bonuses).

The EntityManager maintains separate collections for each entity type and ensures
that all entities are properly added to and removed from the scene.
"""

from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
from entities.bonus import Bonus


class EntityManager:
    """
    Central manager for all game entities.
    
    Responsibilities:
    - Adding new entities to the game world
    - Removing destroyed entities
    - Updating all entities each frame
    - Maintaining separate collections for each entity type
    - Coordinating between entities and the graphics scene
    
    The EntityManager separates entities by type for efficient collision detection
    and targeted updates.
    """

    def __init__(self, scene):
        """
        Initialize the EntityManager.
        
        Args:
            scene (QGraphicsScene): The Qt graphics scene where all entities are rendered.
        """
        self.scene = scene

        self.players = []
        self.enemies = []
        self.bullets = []
        self.bonuses = []

    def add_entity(self, entity):
        """
        Add a new entity to the game world.
        
        Adds the entity to the graphics scene and to the appropriate type collection.
        Raises TypeError if the entity is not a recognized type.
        
        Args:
            entity (GameObject): The entity to add. Must be one of:
                - Player
                - Enemy
                - Bullet
                - Bonus
        
        Raises:
            TypeError: If entity type is not recognized.
        """
        # Add to the graphics scene for rendering
        self.scene.addItem(entity)

        # Add to the appropriate collection based on type
        if isinstance(entity, Player):
            self.players.append(entity)
        elif isinstance(entity, Enemy):
            self.enemies.append(entity)
        elif isinstance(entity, Bullet):
            self.bullets.append(entity)
        elif isinstance(entity, Bonus):
            self.bonuses.append(entity)
        else:
            raise TypeError(
                f"Unsupported entity type: {type(entity).__name__}"
            )

    def remove_entity(self, entity):
        """
        Remove an entity from the game world.
        
        Removes the entity from the graphics scene and from its type collection.
        
        Args:
            entity (GameObject): The entity to remove.
        """
        # Remove from the graphics scene (stops rendering)
        self.scene.removeItem(entity)

        # Remove from the appropriate collection
        for collection in (
            self.players,
            self.enemies,
            self.bullets,
            self.bonuses
        ):
            if entity in collection:
                collection.remove(entity)
                break

    def tick(self):
        """
        Update all entities and remove inactive ones.
        
        This method is called once per frame and:
        1. Calls tick() on every entity to update its state
        2. Removes any entities that are no longer active (marked for destruction)
        
        Processing order: players -> enemies -> bullets -> bonuses
        """
        # Process all entity collections
        for collection in (
            self.players,
            self.enemies,
            self.bullets,
            self.bonuses
        ):
            # Iterate over a copy so we can modify the original during iteration
            for entity in collection[:]:
                # Update the entity's state
                entity.tick()

                # Remove if entity marked for destruction
                if not entity.is_active():
                    self.remove_entity(entity)