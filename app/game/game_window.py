"""
Game Window Module

Manages the main game window and handles user input. Coordinates the game loop timer
and translates keyboard events into game commands. This is the top-level window widget
that contains the graphics view and manages the frame-by-frame game updates.
"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QWidget,
    QGraphicsView,
    QVBoxLayout,
)

from core.game_state import GameState
from game.game_scene import GameScene


class GameWindow(QWidget):
    """
    Main game window and input handler.
    
    Responsibilities:
    - Creating and displaying the game window
    - Running the game loop at 60 FPS
    - Capturing and tracking keyboard input
    - Processing special keys (pause, resume, restart, quit)
    - Managing the graphics view that displays the scene
    
    Attributes:
        WIDTH (int): Window width in pixels (800).
        HEIGHT (int): Window height in pixels (600).
        FPS (int): Target frame rate (60 frames per second).
        scene (GameScene): The game scene being displayed.
        keys (dict): Current state of all tracked keys (True = pressed, False = released).
    """
    
    # Window dimensions
    WIDTH = 800
    HEIGHT = 600

    # Target frame rate
    FPS = 60

    def __init__(self):
        """
        Initialize the game window.
        
        Creates the game scene, initializes the UI, and starts the game loop timer.
        Also sets up the key state tracking dictionary for all input keys.
        """
        super().__init__()

        # Create the game scene
        self.scene = GameScene()

        # Dictionary to track the state of all keyboard keys
        # True = key is pressed down, False = key is released
        self.keys = {
            Qt.Key.Key_Left: False,   # Left arrow
            Qt.Key.Key_Right: False,  # Right arrow
            Qt.Key.Key_A: False,      # A key (left)
            Qt.Key.Key_D: False,      # D key (right)
            Qt.Key.Key_Space: False,  # Spacebar (shoot)
        }

        # Initialize UI layout
        self.init_ui()
        # Start the game loop timer
        self.init_game_loop()

    def init_ui(self):
        """
        Initialize the user interface.
        
        Sets up the window properties, creates the graphics view for rendering,
        and configures its rendering options. Disables scroll bars and sets focus
        policy to accept keyboard input.
        """
        # Set window properties
        self.setWindowTitle("Space Shooter")
        self.setFixedSize(self.WIDTH, self.HEIGHT)

        # Create graphics view to display the scene
        self.view = QGraphicsView(self.scene)
        self.view.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        # Enable antialiasing for smoother graphics
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Disable scroll bars (scene fits in window)
        self.view.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )
        self.view.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Remove frame border
        self.view.setFrameShape(QGraphicsView.Shape.NoFrame)

        # Create layout and add view
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.view)

        self.setLayout(layout)

        # Allow window to receive keyboard focus and events
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)

    def init_game_loop(self):
        """
        Initialize and start the game loop timer.
        
        Creates a QTimer that fires at the target FPS rate (60 times per second),
        calling game_loop() each time. This drives the continuous game updates.
        """
        # Create timer
        self.timer = QTimer()

        # Connect timer timeout signal to game_loop method
        self.timer.timeout.connect(self.game_loop)

        # Calculate interval in milliseconds (1000 ms / 60 fps ≈ 16.67 ms per frame)
        interval = int(1000 / self.FPS)

        # Start the timer
        self.timer.start(interval)

    def game_loop(self):
        """
        Execute one frame of the game loop.
        
        Called 60 times per second by the timer. Processes current key states,
        consolidates them into a single dictionary, and updates the scene.
        
        Key consolidation:
        - Left: A key
        - Right: D key
        - Shoot: Spacebar
        """
        # Consolidate key states into game input format
        keys = {
            "left": self.keys[Qt.Key.Key_Left] or self.keys[Qt.Key.Key_A],
            "right": self.keys[Qt.Key.Key_Right] or self.keys[Qt.Key.Key_D],
            "shoot": self.keys[Qt.Key.Key_Space],
        }

        # Update the scene with current input
        self.scene.update_scene(keys)

    def keyPressEvent(self, event):
        """
        Handle keyboard key press events.
        
        Tracks key states and handles special game commands like pause (ESC),
        resume (C), restart (R), and quit (Q).
        
        Args:
            event (QKeyEvent): The key press event from Qt.
        """
        key = event.key()

        # Track key state if it's one we're monitoring
        if key in self.keys:
            self.keys[key] = True

        # Handle special command keys
        if event.key() == Qt.Key.Key_Escape:
            # ESC to pause
            self.scene.manager.pause()

        if event.key() == Qt.Key.Key_C:
            # C to continue (resume) from pause
            self.scene.manager.resume()

        if event.key() == Qt.Key.Key_R:
            # R to restart from game over
            if self.scene.manager.state == GameState.GAME_OVER:
                self.scene.restart()

        if event.key() == Qt.Key.Key_Q:
            # Q to quit from pause or game over
            if self.scene.manager.state in (
                GameState.PAUSED,
                GameState.GAME_OVER
            ):
                self.close()

    def keyReleaseEvent(self, event):
        """
        Handle keyboard key release events.
        
        Updates key state when a key is released. Only tracks keys that are
        in our monitoring dictionary.
        
        Args:
            event (QKeyEvent): The key release event from Qt.
        """
        key = event.key()

        if key in self.keys:
            self.keys[key] = False