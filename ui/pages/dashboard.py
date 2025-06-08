from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal, sidebar_signal


class DashboardWidget(QWidget):
    def __init__(
            self,
            stack,
            lbl_clock,
            sales_today,
            generic_table_page,
            parent=None
    ):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        sidebar_signal.item_ready.connect(self.refresh_item)
        sidebar_signal.sidebar_ready.connect(self.refresh_sidebar)
        self.lbl_clock = lbl_clock
        self.stack = stack
        self.sales_today = sales_today
        self.generic_table_page = generic_table_page
        self.main = parent
        self.setup_ui()

    def refresh_pages(self):
        self.add_sale_page = StackedManager().get_page_index("AddSaleWidget")
        self.quick_report_page = StackedManager().get_page_index(
            "QuickReportWidget"
        )
        self.report_page = StackedManager().get_page_index("ReportWidget")

    def refresh_sidebar(self, sidebar):
        self.sidebar = sidebar

    def refresh_item(self):
        self.sale_item: int = StackedManager().get_sidebar_index("sales")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(30, 20, 30, 20)

        # --- Header ---
        layout.addLayout(self.create_header())

        # --- Summary Cards ---
        summary_layout = QHBoxLayout()
        self.lbl_box, self.lbl_debt = self.create_summary_cards()
        summary_layout.addWidget(self.lbl_box)
        summary_layout.addWidget(self.lbl_debt)
        summary_layout.addStretch()
        layout.addLayout(summary_layout)

        # --- Buttons ---
        layout.addLayout(self.create_buttons())

        # --- Sales Table ---
        layout.addWidget(self.create_sales_table())

        layout.addStretch()
        self.setLayout(layout)

    def create_header(self):
        header = QHBoxLayout()
        lbl_section = QLabel("لوحة التحكم الرئيسية")
        lbl_section.setFont(QFont("Cairo", 20, QFont.Bold))
        lbl_section.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl_section)
        header.addStretch()
        header.addWidget(self.lbl_clock)
        return header

    def create_summary_cards(self):
        card_style = """
            background-color: #fff;
            border-radius: 12px;
            padding: 20px;
            min-width: 200px;
            min-height: 80px;
            font-size: 18px;
            color: #2d3436;
        """
        lbl_box = QLabel(
            "إجمالي الصندوق<br>"
            "<span style='color:#00b894;'>350,000 ل.س</span>"
        )
        lbl_box.setStyleSheet(card_style)
        lbl_box.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_box.setTextFormat(Qt.TextFormat.RichText)
        lbl_debt = QLabel(
            "إجمالي ديون اليوم<br>"
            "<span style='color:#d35400;'>50,000 ل.س</span>"
        )
        lbl_debt.setStyleSheet(card_style)
        lbl_debt.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_debt.setTextFormat(Qt.TextFormat.RichText)
        return lbl_box, lbl_debt

    def create_buttons(self):
        btn_layout = QHBoxLayout()
        btn_sale = QPushButton("تسجيل بيع جديد")
        btn_sale.clicked.connect(
            # lambda: self.stack.setCurrentIndex(self.add_sale_page)
            self.set_sale_page
        )
        btn_report = QPushButton("تقرير سريع")
        btn_report.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.quick_report_page)
        )
        btn_layout.addWidget(btn_sale)
        btn_layout.addWidget(btn_report)
        btn_layout.addStretch()
        return btn_layout

    def set_sale_page(self):
        self.stack.setCurrentIndex(self.add_sale_page)
        self.sidebar.setCurrentRow(self.sale_item)

    def create_sales_table(self):
        columns = ["التاريخ", "الصنف", "الكمية", "السعر", "الزبون", "تفاصيل"]
        filter_col = 1
        filter_items = ["شامبو", "صابون", "مسحوق غسيل", "مطهر"]
        return self.generic_table_page(
            "مبيعات اليوم", columns, self.sales_today, filter_col, filter_items
        )

    def update_summary(self, box_value, debt_value):
        self.lbl_box.setText(
            f"إجمالي الصندوق<br> \
            <span style='color:#00b894;'>{box_value}</span>"
        )
        self.lbl_debt.setText(
            f"إجمالي ديون اليوم<br> \
            <span style='color:#d35400;'>{debt_value}</span>"
        )
