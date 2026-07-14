from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from game.game_manager import GameManager
from core.game_state import GameState


class GameScene(QGraphicsScene):

    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.initialize()

        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        self.setBackgroundBrush(QBrush(QColor(10, 10, 30)))
        self.score = 0

    def initialize(self):
        self.clear()
        self.frame = 0
        self.create_hud()
        self.manager = GameManager(self)

    def create_hud(self):
        self.info = QGraphicsTextItem()
        self.info.setDefaultTextColor(QColor("white"))
        self.info.setPos(10, 10)
        font = self.info.font()
        font.setPointSize(14)
        font.setBold(True)
        self.info.setFont(font)
        self.addItem(self.info)

    def update_scene(self, keys):
        self.frame += 1
        self.manager.tick(keys)
        self.info.setPlainText(
        f"Score : {self.manager.score}\n"
        f"Record : {self.manager.record}\n"
        f"Enemies : {len(self.manager.entities.enemies)}\n"
        f"Bullets : {len(self.manager.entities.bullets)}\n"
        f"Rapid Fire : {'ON' if self.manager.rapid_fire_timer > 0 else 'OFF'}\n"
        f"Double Score : {'ON' if self.manager.double_score else 'OFF'}\n"
        f"Shield : {'ON' if self.manager.shield_timer > 0 else 'OFF'}"
    )
        if self.manager.state == GameState.PAUSED:
            self.info.setPlainText(
                "PAUSE\n\n"
                "C - Continue\n"
                "Q - Quit"
            )
            return
        elif self.manager.state == GameState.GAME_OVER:
            self.info.setPlainText(
                f"GAME OVER\n\n"
                f"Score : {self.manager.score}\n"
                f"Record : {self.manager.record}\n"
                f"Press R to Restart"
            )
            if(self.manager.score == self.manager.record):
                self.info.setPlainText(
                    f"GAME OVER\n\n"
                    f"Score : {self.manager.score}\n"
                    f"New Record!\n"
                    f"Press R to Restart"
                )
            return
        
    def restart(self):
        self.initialize()