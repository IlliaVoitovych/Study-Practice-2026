from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class ScoreBonus(BonusEffect):

    @property
    def icon(self):
        return "score.png"

    @property
    def name(self):
        return "Score"

    def apply(self, manager):
        manager.score += 100