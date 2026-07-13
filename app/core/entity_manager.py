from entities.player import Player
from entities.enemy import Enemy
from entities.bullet import Bullet
# from entities.bonus import Bonus


class EntityManager:

    def __init__(self, scene):

        self.scene = scene

        self.players = []
        self.enemies = []
        self.bullets = []
        self.bonuses = []

    def add_entity(self, entity):

        self.scene.addItem(entity)

        if isinstance(entity, Player):
            self.players.append(entity)

        elif isinstance(entity, Enemy):
            self.enemies.append(entity)

        elif isinstance(entity, Bullet):
            self.bullets.append(entity)

        # elif isinstance(entity, Bonus):
        #    self.bonuses.append(entity)

        else:
            raise TypeError(
                f"Unsupported entity type: {type(entity).__name__}"
            )

    def remove_entity(self, entity):

        self.scene.removeItem(entity)

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

        for collection in (
            self.players,
            self.enemies,
            self.bullets,
            self.bonuses
        ):

            for entity in collection[:]:

                entity.tick()

                if not entity.is_active():

                    self.remove_entity(entity)