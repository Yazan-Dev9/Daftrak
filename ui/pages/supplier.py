from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton
)
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class SuppliersWidget(QWidget):
    def __init__(self, stack, suppliers, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.suppliers = suppliers
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_supplier_page = StackedManager().get_page_index(
            "AddSupplierWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_suppliers_table())
        self.setLayout(layout)

    # TODO : fix this to use global table
    def _create_suppliers_table(self):
        columns = ["اسم المورد", "رقم الهاتف", "ملاحظات"]
        data = self.suppliers
        filter_col = 0
        filter_items = [row[0] for row in self.suppliers]
        btn_add = QPushButton("إضافة مورد جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_supplier_page)
        )
        return self.generic_table_page(
            "نافذة الموردين", columns, data, filter_col, filter_items, btn_add
        )


class AddSupplierWidget(QWidget):
    def __init__(self, stack, suppliers, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.suppliers = suppliers
        self.setup_ui()

    def refresh_pages(self):
        self.suppliers_page = StackedManager().get_page_index(
            "SuppliersWidget"
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
        lbl = QLabel("إضافة مورد جديد")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.name = QLineEdit()
        self.phone = QLineEdit()
        self.notes = QLineEdit()
        self.form.addRow("اسم المورد:", self.name)
        self.form.addRow("رقم الهاتف:", self.phone)
        self.form.addRow("ملاحظات:", self.notes)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ المورد")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_supplier)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.suppliers_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_supplier(self):
        if self.name.text().strip():
            self.suppliers.append([
                self.name.text(),
                self.phone.text(),
                self.notes.text()
            ])
            self.stack.setCurrentIndex(self.suppliers_page)
        else:
            self.name.setStyleSheet("border:2px solid red;")
