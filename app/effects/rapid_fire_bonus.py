from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class RapidFireBonus(BonusEffect):

    @property
    def icon(self):
        return "rapid_fire.png"

    @property
    def name(self):
        return "Rapid Fire"

    def apply(self, manager):
        manager.player.SHOOT_COOLDOWN = 5
        manager.rapid_fire_timer = 600