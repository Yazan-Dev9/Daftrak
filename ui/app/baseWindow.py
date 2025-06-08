import sys
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QFrame,
)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QSize, QTimer, QTime

from ui.widgets.stackedWidget import StackedWidget
from utils.data import initialize_data
from utils.signals import sidebar_signal
from utils.stackedManager import StackedManager


class MainWindow(QWidget):
    """
    The main window of the application.
    """

    def __init__(self):
        super().__init__()
        self.setWindowTitle("دفترك - برنامج إدارة المحل")
        self.setGeometry(100, 100, 1200, 740)
        self.data = initialize_data()  # Initialize data from file data.py
        self.sidebar_items = {}
        self.load_stylesheet("assets/styles/main.css")
        self.setWindowIcon(QIcon("assets/icons/logo.png"))
        self.setup_ui()

    def load_stylesheet(self, filename):
        """
        Load the stylesheet from the given file.
        """
        try:
            with open(filename, "r") as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            print(f"Error: {filename} not found")

    def setup_ui(self):
        """
        Set up the user interface.
        """
        self.lbl_clock = self.create_clock()
        top_bar = self.create_top_bar()
        self.side_bar = self.create_side_bar()
        stack = StackedWidget(self).create_stacked_widget()

        main_layout = self.create_main_layout(self.side_bar, stack, top_bar)

        self.setLayout(main_layout)

        self.side_bar.currentRowChanged.connect(stack.setCurrentIndex)
        self.side_bar.setCurrentRow(0)

        sidebar_signal.sidebar_ready.emit(self.side_bar)
        sidebar_signal.item_ready.emit()

    def create_clock(self):
        """
        Create the clock widget.
        """
        lbl_clock = QLabel()
        lbl_clock.setFont(QFont("Cairo", 16))
        lbl_clock.setAlignment(Qt.AlignmentFlag.AlignLeft)
        timer = QTimer(self)
        timer.timeout.connect(
            lambda: lbl_clock.setText(
                        f"🕒 {QTime.currentTime().toString('hh:mm A')}")
        )
        timer.start(1000)
        lbl_clock.setText(f"🕒 {QTime.currentTime().toString('hh:mm A')}")
        return lbl_clock

    def create_top_bar(self):
        """
        Create the top bar.
        """
        top_bar = QHBoxLayout()
        lbl_logo = self.create_logo_label(QColor("#00b894"))
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_username = QLabel(f"👤 {self.data['username']}")
        self.lbl_username.setObjectName("User")

        i = 1
        for widget in [lbl_logo, self.lbl_username]:
            top_bar.addWidget(widget)
            if i == 1:
                i = 0
                top_bar.addStretch()
        top_bar.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        top_bar.setSpacing(12)

        separator_line = QFrame()
        separator_line.setObjectName("line")
        separator_line.setFrameShape(QFrame.HLine)

        outer_layout = QVBoxLayout()
        outer_layout.addLayout(top_bar)
        outer_layout.addWidget(separator_line)

        return outer_layout

    def create_logo_label(self, logo_color):
        """
        Create the logo label widget.
        """
        pix_map = self.create_logo_pixmap(logo_color)
        label = QLabel()
        label.setPixmap(pix_map)
        return label

    def create_logo_pixmap(self, logo_color):
        """
        Create the logo pixmap.
        """
        pix_map = QPixmap(250, 100)
        pix_map.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pix_map)
        painter.setRenderHint(QPainter.Antialiasing)

        self.draw_logo_elements(painter, logo_color)

        painter.end()
        return pix_map

    def draw_logo_elements(self, painter, logo_color):
        """
        Draw all elements of the logo.
        """
        # Draw the book icon
        painter.setBrush(QColor(230, 240, 255))
        painter.setPen(QColor(52, 152, 219))
        painter.drawRoundedRect(15, 20, 60, 60, 12, 12)
        painter.setPen(QColor(180, 180, 180))
        for y in range(35, 70, 10):
            painter.drawLine(25, y, 65, y)

        # Draw the dollar sign
        painter.setBrush(logo_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(55, 60, 22, 22)
        painter.setPen(Qt.GlobalColor.white)
        font = QFont("Arial", 14, QFont.Bold)
        painter.setFont(font)
        painter.drawText(55, 60, 22, 22, Qt.AlignmentFlag.AlignCenter, "$")

        # Write the program name
        painter.setPen(logo_color)
        font = QFont("Arial", 32, QFont.Bold)
        painter.setFont(font)
        painter.drawText(100, 60, "دفتـرك")

        # Write the slogan
        painter.setPen(QColor(52, 152, 219))
        font = QFont("Arial", 14)
        painter.setFont(font)
        painter.drawText(104, 85, "بساطة نمو ازدهار")

    def create_side_bar(self):
        """
        Create the side bar.
        """
        sidebar = QListWidget()
        sidebar.setFixedWidth(190)
        sidebar.setIconSize(QSize(32, 32))
        sidebar.setLayoutDirection(Qt.LayoutDirection.RightToLeft)

        menu_items = [
            ("الصفحة الرئيسية", "assets/icons/home.png", "home"),
            ("المبيعات", "assets/icons/money.png", "sales"),
            ("المشتريات", "assets/icons/shopping-cart.png", "purchases"),
            ("المخزون", "assets/icons/inventory.png", "inventory"),
            ("الجرد", "assets/icons/clipboard.png", "stock"),
            ("الديون", "assets/icons/debt.png", "debts"),
            ("الزبائن", "assets/icons/customer.png", "customers"),
            ("الموردين", "assets/icons/truck.png", "suppliers"),
            ("التقارير", "assets/icons/bar-chart.png", "reports"),
            ("الإعدادات", "assets/icons/settings.png", "settings"),
        ]

        i = 0
        for title, icon_path, name in menu_items:
            item = QListWidgetItem(QIcon(icon_path), "  " + title)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setSizeHint(QSize(170, 50))
            self.sidebar_items[name] = i
            i += 1
            sidebar.addItem(item)

        StackedManager().set_sidebar_items(self.sidebar_items)

        return sidebar

    def create_main_layout(self, side_bar, stack, top_bar):
        """
        Create the main layout.
        """
        main_layout = QHBoxLayout()
        main_layout.addWidget(side_bar)
        main_layout.addWidget(stack, stretch=1)

        outer_layout = QVBoxLayout()
        outer_layout.addLayout(top_bar)
        outer_layout.addLayout(main_layout)

        return outer_layout


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
