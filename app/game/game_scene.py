"""
Game Scene Module

Manages the Qt graphics scene where all game entities are rendered and displayed.
Handles HUD (heads-up display) updates and game state-specific UI rendering.
Acts as the bridge between the GameManager logic and the graphical presentation.
"""

from PyQt6.QtGui import QColor, QBrush
from PyQt6.QtWidgets import (
    QGraphicsScene,
    QGraphicsTextItem,
)

from game.game_manager import GameManager
from core.game_state import GameState
from core.resource_manager import ResourceManager


class GameScene(QGraphicsScene):
    """
    Qt graphics scene containing all game entities and HUD elements.
    
    Responsibilities:
    - Rendering the game background
    - Updating and displaying HUD information (score, bonuses, instructions)
    - Rendering different UI based on game state (PLAYING, PAUSED, GAME_OVER)
    - Managing the GameManager instance
    - Handling scene restart
    
    Attributes:
        WIDTH (int): Scene width in pixels (800).
        HEIGHT (int): Scene height in pixels (600).
        manager (GameManager): The game logic controller.
        info (QGraphicsTextItem): Text overlay for HUD and messages.
    """

    # Scene dimensions
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        """
        Initialize the game scene.
        
        Sets up the scene dimensions, background image, and initializes the
        GameManager to begin the game state.
        """
        super().__init__()
        self.initialize()

        # Set scene boundaries and background image
        self.setSceneRect(0, 0, self.WIDTH, self.HEIGHT)
        self.setBackgroundBrush(QBrush(ResourceManager.load_pixmap("background.png")))
        self.score = 0

    def initialize(self):
        """
        Reset the game scene to initial state.
        
        Clears all entities, resets frame counter, recreates HUD,
        and creates a new GameManager to start fresh gameplay.
        """
        # Clear all entities from the scene
        self.clear()
        # Reset frame counter
        self.frame = 0
        # Recreate HUD text display
        self.create_hud()
        # Create new game manager (starts fresh game)
        self.manager = GameManager(self)

    def create_hud(self):
        """
        Create the HUD (heads-up display) text element.
        
        Initializes the text display that shows score, record, and bonus status.
        Styles it with white color, positioned at top-left, and bold font.
        """
        # Create text item for HUD
        self.info = QGraphicsTextItem()
        self.info.setDefaultTextColor(QColor("white"))
        self.info.setPos(10, 10)
        # Set font styling
        font = self.info.font()
        font.setPointSize(14)
        font.setBold(True)
        self.info.setFont(font)
        # Add to scene
        self.addItem(self.info)

    def update_scene(self, keys):
        """
        Update the scene for one frame.
        
        Called every frame by the game loop. Handles game logic updates,
        HUD rendering based on game state, and state-specific UI display.
        
        HUD displays:
        - PLAYING: Score, record, active bonus statuses
        - PAUSED: Pause menu with continue/quit instructions
        - GAME_OVER: Final score, record, restart/quit instructions
        
        Args:
            keys (dict): Current keyboard input state.
        """
        # Increment frame counter
        self.frame += 1
        
        # Update game logic
        self.manager.tick(keys)
        
        # Update HUD with current game state
        self.info.setPlainText(
        f"Score : {self.manager.score}\n"
        f"Record : {self.manager.record}\n"
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
        # Display game over screen
        elif self.manager.state == GameState.GAME_OVER:
            self.info.setPlainText(
                f"GAME OVER\n\n"
                f"Score : {self.manager.score}\n"
                f"Record : {self.manager.record}\n"
                f"Press R to Restart\n"
                f"Press Q to Quit\n"
            )
            if(self.manager.score == self.manager.record):
                self.info.setPlainText(
                    f"GAME OVER\n\n"
                    f"Score : {self.manager.score}\n"
                    f"New Record!\n"
                    f"Press R to Restart\n"
                    f"Press Q to Quit\n"
                )
            return
        
    def restart(self):
        """
        Restart the game by reinitializing the scene.
        
        Clears all current game state and creates a fresh new game.
        """
        self.initialize()