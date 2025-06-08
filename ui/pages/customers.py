from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QFormLayout,
    QLineEdit,
)
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class CustomersWidget(QWidget):
    def __init__(self, stack, customers, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.customers = customers
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_customer_page = StackedManager().get_page_index(
            "AddCustomerWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_customers_table())
        self.setLayout(layout)

    def _create_customers_table(self):
        columns = ["اسم الزبون", "رقم الهاتف", "ديون", "تفاصيل"]
        data = self.customers
        filter_col = 0
        filter_items = [row[0] for row in self.customers]
        btn_add = QPushButton("إضافة زبون جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_customer_page)
        )
        return self.generic_table_page(
            "نافذة الزبائن", columns, data, filter_col, filter_items, btn_add
        )


class AddCustomerWidget(QWidget):
    def __init__(self, stack, customers, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.customers = customers
        self.setup_ui()

    def refresh_pages(self):
        self.customers_page = StackedManager().get_page_index(
            "CustomersWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_form())
        layout.addLayout(self._create_buttons())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("إضافة زبون جديد")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.debt = QLineEdit()
        self.form.addRow("الاسم:", self.name)
        self.form.addRow("رقم الهاتف:", self.phone)
        self.form.addRow("دين ابتدائي:", self.debt)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ الزبون")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_customer)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.customers_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_customer(self):
        self.customers.append(
            [
                self.name.text(),
                self.phone.text(),
                self.debt.text(),
                "",
            ]
        )
        self.stack.setCurrentIndex(self.customers_page)
