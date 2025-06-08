from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QComboBox,
    QSpinBox,
)
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class PurchasesWidget(QWidget):
    def __init__(self, stack, purchases, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.purchases = (
            purchases
        )
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_purchase_page = StackedManager().get_page_index(
            "AddPurchaseWidget"
        )

    def setup_ui(self):
        btn_add = QPushButton("شراء جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_purchase_page)
        )

        columns = ["الصنف", "المورد", "الكمية", "سعر الوحدة", "الإجمالي"]
        filter_col = 0
        filter_items = (
            list({row[0] for row in self.purchases}) if self.purchases else []
        )

        table_page = self.generic_table_page(
            "جدول المشتريات",
            columns, self.purchases,
            filter_col,
            filter_items,
            btn_add
        )

        layout = QVBoxLayout()
        layout.addWidget(table_page)
        layout.addStretch()
        self.setLayout(layout)

    def refresh(self):
        self.setup_ui()


class AddPurchaseWidget(QWidget):
    def __init__(self, stack, products, suppliers, purchases, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.products = products
        self.suppliers = suppliers
        self.purchases = purchases
        self.setup_ui()

    def refresh_pages(self):
        self.purchases_page = StackedManager().get_page_index(
            "PurchasesWidget"
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
        lbl = QLabel("تسجيل عملية شراء جديدة")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.product_combo = QComboBox()
        self.product_combo.addItems([row[0] for row in self.products])
        self.supplier_combo = QComboBox()
        self.supplier_combo.addItems([row[0] for row in self.suppliers])
        self.qty = QSpinBox()
        self.qty.setRange(1, 10000)
        self.price = QLineEdit()
        self.total = QLineEdit()
        self.total.setReadOnly(True)

        self.form.addRow("الصنف:", self.product_combo)
        self.form.addRow("المورد:", self.supplier_combo)
        self.form.addRow("الكمية:", self.qty)
        self.form.addRow("سعر الوحدة:", self.price)
        self.form.addRow("الإجمالي:", self.total)

        self.qty.valueChanged.connect(self.calc_total)
        self.price.textChanged.connect(self.calc_total)

        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ عملية الشراء")
        btn_save.clicked.connect(self.save_purchase)
        btn_back = QPushButton("رجوع")
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.purchases_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def calc_total(self):
        try:
            total = int(self.qty.value()) * float(self.price.text())
            self.total.setText(str(total))
        except Exception:
            self.total.setText("")

    def save_purchase(self):
        self.purchases.append(
            [
                self.product_combo.currentText(),
                self.supplier_combo.currentText(),
                str(self.qty.value()),
                self.price.text(),
                self.total.text(),
            ]
        )
        self.stack.setCurrentIndex(self.purchases_page)
