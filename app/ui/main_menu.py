"""
Main Menu Module

Provides the main menu UI for the Space Shooter game. Displays the title,
Start button, and Exit button. Handles the transition from menu to gameplay.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QPushButton,
    QLabel,
    QVBoxLayout,
)

from game.game_window import GameWindow


class MainMenu(QWidget):
    """
    Main menu user interface.
    
    Displays a styled menu with:
    - Game title ("SPACE SHOOTER")
    - Start button to begin gameplay
    - Exit button to quit the application
    """

    def __init__(self):
        """
        Initialize the main menu window.
        
        Sets up the UI layout and styling. The window remains visible until
        the player clicks Start (which creates and shows the game window)
        or Exit (which closes the application).
        """
        super().__init__()

        self.game_window = None

        self.init_ui()

    def init_ui(self):
        """
        Initialize the menu user interface.
        
        Creates and styles the menu components including the title, buttons,
        and layout. Uses a vertical layout with spacing and margins for
        proper visual arrangement.
        """
        # Set window properties
        self.setWindowTitle("Space Shooter")
        self.setFixedSize(900, 700)

        self.setStyleSheet("""
            QWidget{
                background-color:#101820;
            }

            QLabel{
                color:white;              
                font-size:34px;
                font-weight:bold;
            }

            QPushButton{
                background:#2E86DE;
                color:white;
                font-size:18px;
                border-radius:8px;
                min-height:45px;
            }

            QPushButton:hover{
                background:#54A0FF;
            }
        """)

        # Create title label
        title = QLabel("SPACE SHOOTER")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        start_button = QPushButton("Старт")
        exit_button = QPushButton("Вихід")

        start_button.clicked.connect(self.start_game)
        exit_button.clicked.connect(self.close)

        layout = QVBoxLayout()

        # Add stretch to center content vertically
        layout.addStretch()

        # Add title with spacing
        layout.addWidget(title)
        layout.addSpacing(40)

        # Add buttons
        layout.addWidget(start_button)
        layout.addWidget(exit_button)

        # Add bottom stretch
        layout.addStretch()

        # Set layout margins (left, top, right, bottom)
        layout.setContentsMargins(200, 60, 200, 60)

        self.setLayout(layout)

    def start_game(self):
        """
        Handle Start button click.
        
        Creates a new game window and displays it, then closes the menu.
        The game window is stored in self.game_window to maintain a reference
        (preventing garbage collection).
        """
        # Create new game window
        self.game_window = GameWindow()
        # Display the game window
        self.game_window.show()
        # Close the menu window
        self.close()