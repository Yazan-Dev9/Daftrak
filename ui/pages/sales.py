from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFormLayout, QComboBox,
    QSpinBox, QLineEdit, QPushButton
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class SalesWidget(QWidget):
    def __init__(self, stack, sales_today, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.sales_today = sales_today
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_sale_page = StackedManager().get_page_index("AddSaleWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_sales_table())
        self.setLayout(layout)

    def _create_sales_table(self):
        columns = ["التاريخ", "الصنف", "الكمية", "السعر", "الزبون", "تفاصيل"]
        data = self.sales_today
        filter_col = 1
        filter_items = ["شامبو", "صابون", "مسحوق غسيل", "مطهر"]
        btn_add = QPushButton("إضافة عملية بيع جديدة")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_sale_page)
        )
        return self.generic_table_page(
            "نافذة المبيعات", columns, data, filter_col, filter_items, btn_add
        )


class AddSaleWidget(QWidget):
    def __init__(self, stack, products, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.products = products
        self.products_prices = {row[0]: row[4] for row in self.products}
        self.setup_ui()

    def refresh_pages(self):
        self.sales_page = StackedManager().get_page_index("SalesWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(30, 20, 30, 20)

        layout.addLayout(self._create_header())
        layout.addLayout(self._create_form())
        layout.addLayout(self._create_buttons())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("تسجيل بيع جديد")
        lbl.setProperty("role", "header")
        lbl.setFont(QFont("Cairo", 20, QFont.Bold))
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form_layout = QFormLayout()
        self.form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.product_combo = QComboBox()
        self.product_combo.setEditable(True)
        self.product_combo.addItems(self.products_prices.keys())

        self.qty = QSpinBox()
        self.qty.setRange(1, 1000)

        self.price = QLineEdit()
        self.total_price = QLineEdit()
        self.customer = QLineEdit()
        self.customer.setText("زبون نقدي")
        self.total_price.setReadOnly(True)

        self.form_layout.addRow("الصنف:", self.product_combo)
        self.form_layout.addRow("الكمية:", self.qty)
        self.form_layout.addRow("سعر البيع:", self.price)
        self.form_layout.addRow("السعر الكلي:", self.total_price)
        self.form_layout.addRow("اسم الزبون:", self.customer)

        self.product_combo.currentTextChanged.connect(self.update_price)
        self.qty.valueChanged.connect(self.calc_total)
        self.price.textChanged.connect(self.calc_total)

        self.update_price()

        return self.form_layout

    def _create_buttons(self):
        btn_layout = QHBoxLayout()
        btn_save = QPushButton("حفظ البيع")
        btn_back = QPushButton("رجوع")
        btn_layout.addStretch()
        btn_layout.addWidget(btn_save)
        btn_layout.addWidget(btn_back)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.sales_page)
        )
        return btn_layout

    def update_price(self):
        prod = self.product_combo.currentText()
        val = self.products_prices.get(prod, "")
        self.price.setText(str(val))
        self.calc_total()

    def calc_total(self):
        try:
            quantity = self.qty.value()
            unit_price = int(
                self.price.text()
            ) if self.price.text().isdigit() else 0

            total = quantity * unit_price
            self.total_price.setText(str(total))
        except Exception:
            self.total_price.setText("0")


class DebtsWidget(QWidget):
    def __init__(self, stack, debts, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.debts = debts
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_debt_page = StackedManager().get_page_index("AddDebtWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_debts_table())
        self.setLayout(layout)

    def _create_debts_table(self):
        columns = ["الزبون", "المبلغ", "التاريخ", "الحالة", "تفاصيل"]
        data = self.debts
        filter_col = 0
        filter_items = ["أبو علي", "أم محمد"]
        btn_add = QPushButton("إضافة دين جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_debt_page)
        )
        return self.generic_table_page(
            "نافذة الديون", columns, data, filter_col, filter_items, btn_add
        )


class AddDebtWidget(QWidget):
    def __init__(self, stack, debts, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.debts = debts
        self.setup_ui()

    def refresh_pages(self):
        self.debts_page = StackedManager().get_page_index("DebtsWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_form())
        layout.addLayout(self._create_buttons())
        layout.addWidget(self._create_message())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("إضافة دين جديد")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.customer = QLineEdit()
        self.amount = QLineEdit()
        self.date = QLineEdit()
        self.status = QLineEdit()
        self.details = QLineEdit()
        self.form.addRow("اسم الزبون:", self.customer)
        self.form.addRow("المبلغ:", self.amount)
        self.form.addRow("التاريخ:", self.date)
        self.form.addRow("الحالة:", self.status)
        self.form.addRow("تفاصيل:", self.details)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ الدين")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_debt)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.debts_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def _create_message(self):
        self.msg = QLabel("")
        self.msg.setStyleSheet("color: red;")
        return self.msg

    def save_debt(self):
        if self.customer.text().strip() == "":
            self.msg.setText("يجب إدخال اسم الزبون!")
            return
        self.debts.append([
            self.customer.text(),
            self.amount.text(),
            self.date.text(),
            self.status.text(),
            self.details.text(),
        ])
        self.msg.setText("")
        self.stack.setCurrentIndex(self.debts_page)
