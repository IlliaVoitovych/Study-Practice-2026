import random
from effects.score_bonus import ScoreBonus
from effects.rapid_fire_bonus import RapidFireBonus
from effects.double_score_bonus import DoubleScoreBonus
from effects.shield_bonus import ShieldBonus
from PyQt6.QtCore import QRectF
from PyQt6.QtGui import QColor, QBrush, QPen
from core.game_object import GameObject

effects = [
    ScoreBonus,
    RapidFireBonus,
    DoubleScoreBonus,
    ShieldBonus
]

class Bonus(GameObject):

    SIZE = 25
    SPEED = 2

    def __init__(self, scene_width):
        super().__init__()

        x = random.randint(0, scene_width - self.SIZE)

        self.setPos(x, -self.SIZE)
        self.effect = random.choice(effects)()

    def boundingRect(self):
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.effect.color))
        painter.setPen(QPen(QColor("white"), 2))
        painter.drawEllipse(0, 0, self.SIZE, self.SIZE)

    def tick(self):

        self.setY(
            self.y() + self.SPEED
        )

        if self.y() > 650:
            self.destroy()