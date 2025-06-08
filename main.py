import sys
from ui.app.baseWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


def main(*args):
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
