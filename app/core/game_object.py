from PyQt6.QtWidgets import QGraphicsItem


class GameObject(QGraphicsItem):
    """
    Базовий клас для всіх ігрових об'єктів.
    """

    def __init__(self):
        super().__init__()

        self.active = True

    def destroy(self):
        self.active = False

    def is_active(self):
        return self.active

    def tick(self, *args, **kwargs):
        """
        Перевизначається у похідних класах.
        """
        pass