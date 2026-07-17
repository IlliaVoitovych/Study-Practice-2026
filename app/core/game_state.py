"""
Game State Enumeration

Defines all possible states the game can be in during its lifecycle.
These states control which update logic is executed and which UI elements are displayed.
"""

from enum import Enum, auto


class GameState(Enum):
    """
    Enumeration of all possible game states.
    
    States:
        MENU: Main menu is displayed, game is not running.
        PLAYING: Game is actively running, updating all game logic.
        GAME_OVER: Game has ended due to collision, displaying game over screen.
        PAUSED: Game is paused, game logic is frozen but UI remains visible.
    """
    MENU = auto()
    PLAYING = auto()
    GAME_OVER = auto()
    PAUSED = auto()