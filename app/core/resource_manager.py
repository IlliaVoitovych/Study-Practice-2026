from pathlib import Path

from PyQt6.QtGui import QPixmap


class ResourceManager:
    BASE_DIR = Path(__file__).resolve().parent.parent
    ASSETS = BASE_DIR / "assets"
    @classmethod
    def load_pixmap(cls, *parts):
        path = cls.ASSETS.joinpath(*parts)
        return QPixmap(str(path))