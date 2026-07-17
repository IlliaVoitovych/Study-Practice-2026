"""
Space Shooter Game - Main Entry Point

This module serves as the entry point for the Space Shooter game application.
It initializes the PyQt6 appliication and displays the main menu window.
"""

import sys
from PyQt6.QtWidgets import QApplication
from ui.main_menu import MainMenu


def main():
    """
    Initialize and run the Space Shooter game application.
    
    Creates the QApplication instance, displays the main menu window,
    and starts the Qt event loop.
    """
    app = QApplication(sys.argv)
    window = MainMenu()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()