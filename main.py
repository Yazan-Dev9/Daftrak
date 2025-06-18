import sys
from ui.app.baseWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from database.connection import db
# from models.user import User


def main(*args):
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    db.init_db()
    main(sys.argv)
