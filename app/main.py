import sys

from PyQt6.QtWidgets import QApplication

from ui.main_menu import MainMenu


def main():
    app = QApplication(sys.argv)

    window = MainMenu()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()