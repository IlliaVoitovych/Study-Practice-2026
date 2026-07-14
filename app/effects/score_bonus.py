from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class ScoreBonus(BonusEffect):

    @property
    def color(self):
        return QColor("green")

    @property
    def name(self):
        return "Score"

    def apply(self, manager):
        manager.score += 100