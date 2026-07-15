import random
from core.resource_manager import ResourceManager
from effects.score_bonus import ScoreBonus
from effects.rapid_fire_bonus import RapidFireBonus
from effects.double_score_bonus import DoubleScoreBonus
from effects.shield_bonus import ShieldBonus
from PyQt6.QtCore import QRectF, Qt
from core.game_object import GameObject

effects = [
    ScoreBonus,
    RapidFireBonus,
    DoubleScoreBonus,
    ShieldBonus
]

class Bonus(GameObject):

    SIZE = 35
    SPEED = 2

    def __init__(self, scene_width):
        super().__init__()

        x = random.randint(0, scene_width - self.SIZE)

        self.setPos(x, -self.SIZE)
        self.effect = random.choice(effects)()
        self.sprite = ResourceManager.load_pixmap(
            self.effect.icon).scaled(
            self.SIZE,
            self.SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def boundingRect(self):
        return QRectF(0, 0, self.SIZE, self.SIZE)

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(
            self.boundingRect().toRect(),
            self.sprite
        )

    def tick(self):

        self.setY(
            self.y() + self.SPEED
        )

        if self.y() > 650:
            self.destroy()