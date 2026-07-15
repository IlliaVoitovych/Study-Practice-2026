from abc import ABC, abstractmethod
from PyQt6.QtGui import QColor


class BonusEffect(ABC):

    @property
    @abstractmethod
    def icon(self):
        """Іконка бонусу."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Назва бонусу."""
        pass

    @abstractmethod
    def apply(self, manager):
        """Застосувати ефект бонусу."""
        pass