"""
Resource Manager Module

This module provides centralized resource loading functionality for the game,
specifically handling image asset loading from the assets directory.
"""

from pathlib import Path
from PyQt6.QtGui import QPixmap


class ResourceManager:
    """
    Centralized manager for loading game resources (images, sprites).
    """
    BASE_DIR = Path(__file__).resolve().parent.parent
    # Assets directory path
    ASSETS = BASE_DIR / "assets"

    @classmethod
    def load_pixmap(cls, *parts):
        """
        Load an image file from the assets directory as a QPixmap.
        
        Constructs the full file path using the provided path components
        and loads it as a PyQt6 QPixmap object suitable for rendering.
        
        Args:
            *parts: Path components relative to the assets directory.        
        Returns:
            QPixmap: A Qt image object ready to be scaled and rendered.
        """
        path = cls.ASSETS.joinpath(*parts)
        return QPixmap(str(path))