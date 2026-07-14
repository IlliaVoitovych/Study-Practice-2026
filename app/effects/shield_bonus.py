from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class ShieldBonus(BonusEffect):

    @property
    def color(self):
        return QColor("magenta")

    @property
    def name(self):
        return "Shield"

    def apply(self, manager):
        manager.shield_timer = 600