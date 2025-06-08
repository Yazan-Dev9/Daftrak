from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QTableWidget,
    QHeaderView,
    QTableWidgetItem,
    QFormLayout,
    QLineEdit,
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from utils.data import initialize_data
from utils.stackedManager import StackedManager
from utils.signals import pages_signal, sidebar_signal


class QuickReportWidget(QWidget):
    def __init__(self, stack, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        sidebar_signal.item_ready.connect(self.refresh_item)
        sidebar_signal.sidebar_ready.connect(self.refresh_sidebar)
        self.stack = stack
        self.setup_ui()

    def refresh_pages(self):
        self.back_page = StackedManager().get_page_index("DashboardWidget")

    def refresh_sidebar(self, sidebar):
        self.sidebar = sidebar

    def refresh_item(self):
        self.report_item: int = StackedManager().get_sidebar_index("reports")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_report_labels())
        layout.addLayout(self._create_back_button())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QHBoxLayout()
        lbl = QLabel("تقرير سريع")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_report_labels(self):
        labels_layout = QVBoxLayout()
        self.lbl1 = QLabel("مبيعات اليوم: 80,000 ل.س")
        self.lbl2 = QLabel("مبيعات هذا الأسبوع: 400,000 ل.س")
        self.lbl3 = QLabel("مبيعات هذا الشهر: 1,200,000 ل.س")
        self.lbl4 = QLabel("أكثر صنف مبيعاً: شامبو")
        for lb in [self.lbl1, self.lbl2, self.lbl3, self.lbl4]:
            lb.setFont(QFont("Cairo", 15))
            lb.setAlignment(Qt.AlignmentFlag.AlignRight)
            labels_layout.addWidget(lb)
        return labels_layout

    def _create_back_button(self):
        btn_layout = QHBoxLayout()
        btn_back = QPushButton("رجوع")
        btn_back.clicked.connect(
            self.set_report_page
        )
        btn_layout.addWidget(btn_back, alignment=Qt.AlignmentFlag.AlignLeft)
        return btn_layout

    def set_report_page(self):
        self.stack.setCurrentIndex(self.back_page)
        self.sidebar.setCurrentRow(self.report_item)

    def update_report(self, today, week, month, top_item):
        self.lbl1.setText(f"مبيعات اليوم: {today}")
        self.lbl2.setText(f"مبيعات هذا الأسبوع: {week}")
        self.lbl3.setText(f"مبيعات هذا الشهر: {month}")
        self.lbl4.setText(f"أكثر صنف مبيعاً: {top_item}")


class ReportsWidget(QWidget):
    def __init__(self, stack, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.setup_ui()
        self.setup_data()
        self.update_report()

    def refresh_pages(self):
        self.add_report_page = StackedManager().get_page_index(
            "AddReportWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_report_type_combo())
        layout.addWidget(self._create_table())
        layout.addLayout(self._create_add_button())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QHBoxLayout()
        lbl = QLabel("نافذة التقارير")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_report_type_combo(self):
        combo_layout = QHBoxLayout()
        self.report_type_combo = QComboBox()
        self.report_type_combo.addItems(
            [
                    "تقرير يومي",
                    "تقرير أسبوعي",
                    "تقرير شهري"
                ]
        )
        self.report_type_combo.currentIndexChanged.connect(self.update_report)
        combo_layout.addWidget(
            self.report_type_combo, alignment=Qt.AlignmentFlag.AlignRight
        )
        return combo_layout

    def _create_table(self):
        self.report_table = QTableWidget()
        self.report_table.setColumnCount(6)
        self.report_table.setHorizontalHeaderLabels(
            ["التاريخ", "الصنف", "الكمية", "الإجمالي", "الزبون", "تفاصيل"]
        )
        self.report_table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignRight
        )
        self.report_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch
        )
        return self.report_table

    def _create_add_button(self):
        btn_layout = QHBoxLayout()
        btn_add = QPushButton("تقرير جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_report_page)
        )
        btn_layout.addWidget(btn_add, alignment=Qt.AlignmentFlag.AlignLeft)
        return btn_layout

    def setup_data(self):
        self.daily = initialize_data().get("daily")
        self.weekly = initialize_data().get("weekly")
        self.monthly = initialize_data().get("monthly")

    def fill_table(self, data):
        self.report_table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col != 5:
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.report_table.setItem(row, col, item)

    def update_report(self):
        report_type = self.report_type_combo.currentIndex()
        if report_type == 0:
            self.fill_table(self.daily)
        elif report_type == 1:
            self.fill_table(self.weekly)
        else:
            self.fill_table(self.monthly)

    def set_data(self, daily, weekly, monthly):
        self.daily = daily
        self.weekly = weekly
        self.monthly = monthly
        self.update_report()


class AddReportWidget(QWidget):
    def __init__(self, stack, reports, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.reports = reports
        self.setup_ui()

    def refresh_pages(self):
        self.reports_page = StackedManager().get_page_index("ReportsWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_form())
        layout.addLayout(self._create_buttons())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("إضافة تقرير جديد")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.kind = QLineEdit()
        self.period = QLineEdit()
        self.total = QLineEdit()
        self.details = QLineEdit()
        self.notes = QLineEdit()
        self.form.addRow("نوع التقرير:", self.kind)
        self.form.addRow("الفترة:", self.period)
        self.form.addRow("الإجمالي:", self.total)
        self.form.addRow("تفاصيل:", self.details)
        self.form.addRow("ملاحظات:", self.notes)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ التقرير")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_report)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.reports_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_report(self):
        self.reports.append(
            [
                self.kind.text(),
                self.period.text(),
                self.total.text(),
                self.details.text(),
                self.notes.text(),
            ]
        )
        self.stack.setCurrentIndex(self.reports_page)
