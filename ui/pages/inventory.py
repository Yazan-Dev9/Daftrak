from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFormLayout, QLineEdit, QPushButton,
)
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class InventoryWidget(QWidget):
    def __init__(self, stack, products, generic_table_page, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.products = products
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_product_page = StackedManager().get_page_index(
            "AddProductWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_inventory_table())
        self.setLayout(layout)

    def _create_inventory_table(self):
        columns = [
            "الصنف",
            "الوحدة",
            "الكمية",
            "سعر الشراء",
            "سعر البيع",
            "تفاصيل"
        ]
        data = self.products
        filter_col = 0
        filter_items = [row[0] for row in self.products]
        btn_add = QPushButton("إضافة صنف جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_product_page)
        )
        return self.generic_table_page(
            "نافذة المخزون", columns, data, filter_col, filter_items, btn_add
        )


class AddProductWidget(QWidget):
    def __init__(self, stack, products, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.products = products
        self.setup_ui()

    def refresh_pages(self):
        self.inventory_page = StackedManager().get_page_index(
            "InventoryWidget"
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
        lbl = QLabel("إضافة صنف جديد للمخزن")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.name = QLineEdit()
        self.unit = QLineEdit()
        self.qty = QLineEdit()
        self.buy_price = QLineEdit()
        self.sell_price = QLineEdit()
        self.form.addRow("اسم الصنف:", self.name)
        self.form.addRow("الوحدة:", self.unit)
        self.form.addRow("الكمية:", self.qty)
        self.form.addRow("سعر الشراء:", self.buy_price)
        self.form.addRow("سعر البيع:", self.sell_price)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ الصنف")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_product)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.inventory_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_product(self):
        self.products.append([
            self.name.text(),
            self.unit.text(),
            self.qty.text(),
            self.buy_price.text(),
            self.sell_price.text()
        ])
        self.stack.setCurrentIndex(self.inventory_page)


class StocktakingWidget(QWidget):
    def __init__(
            self,
            stack,
            stocktaking_data,
            generic_table_page,
            parent=None
    ):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.stocktaking_data = stocktaking_data
        self.generic_table_page = generic_table_page
        self.setup_ui()

    def refresh_pages(self):
        self.add_stocktaking_page = StackedManager().get_page_index(
            "AddStocktakingWidget"
        )

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self._create_stocktaking_table())
        self.setLayout(layout)

    def _create_stocktaking_table(self):
        columns = ["الصنف", "الكمية المسجلة", "الكمية الفعلية", "تفاصيل"]
        data = self.stocktaking_data
        filter_col = 0
        filter_items = ["شامبو", "صابون", "مسحوق غسيل", "مطهر"]
        btn_add = QPushButton("جرد جديد")
        btn_add.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.add_stocktaking_page)
        )
        return self.generic_table_page(
            "نافذة الجرد", columns, data, filter_col, filter_items, btn_add
        )


class AddStocktakingWidget(QWidget):
    def __init__(self, stack, stocktaking_data, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.stocktaking_data = stocktaking_data
        self.setup_ui()

    def refresh_pages(self):
        self.stocktaking_page = StackedManager().get_page_index(
            "StocktakingWidget"
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
        lbl = QLabel("جرد جديد")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.product = QLineEdit()
        self.old_qty = QLineEdit()
        self.real_qty = QLineEdit()
        self.details = QLineEdit()
        self.form.addRow("الصنف:", self.product)
        self.form.addRow("الكمية المسجلة:", self.old_qty)
        self.form.addRow("الكمية الفعلية:", self.real_qty)
        self.form.addRow("تفاصيل:", self.details)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ الجرد")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_stocktaking)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.stocktaking_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_stocktaking(self):
        self.stocktaking_data.append([
            self.product.text(),
            self.old_qty.text(),
            self.real_qty.text(),
            self.details.text()
        ])
        self.stack.setCurrentIndex(self.stocktaking_page)
