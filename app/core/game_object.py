from abc import ABC, abstractmethod

from PyQt6.QtCore import QRectF
from PyQt6.QtWidgets import QGraphicsItem


class GameObject(QGraphicsItem, ABC):
    """
    Базовий клас для всіх ігрових об'єктів.
    """

    def __init__(self):
        super().__init__()

        self.active = True

    @abstractmethod
    def boundingRect(self) -> QRectF:
        pass

    @abstractmethod
    def paint(self, painter, option, widget=None):
        pass

    @abstractmethod
    def update(self):
        """
        Оновлення oб'єкта кожен кадр.
        """
        pass

    def destroy(self):
        """
        Позначає oб'єкт як неактивний.
        """
        self.active = False

    def is_active(self):
        return self.active