from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class DoubleScoreBonus(BonusEffect):

    @property
    def icon(self):
        return "double_score.png"

    @property
    def name(self):
        return "Double Score"

    def apply(self, manager):
        manager.double_score = True
        manager.double_score_timer = 600