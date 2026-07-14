from PyQt6.QtGui import QColor

from effects.bonus_effect import BonusEffect


class DoubleScoreBonus(BonusEffect):

    @property
    def color(self):
        return QColor("cyan")

    @property
    def name(self):
        return "Double Score"

    def apply(self, manager):
        manager.double_score = True
        manager.double_score_timer = 600