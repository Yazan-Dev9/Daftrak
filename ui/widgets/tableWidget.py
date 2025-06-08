from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QComboBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class TableWidget(QWidget):
    def __init__(
            self,
            title,
            columns,
            data,
            filter_col=None,
            filter_items=None,
            add_btn=None,
            parent=None
    ):
        super().__init__(parent)
        self.title = title
        self.columns = columns
        self.data = data
        self.filter_col = filter_col
        self.filter_items = filter_items
        self.add_btn = add_btn
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_search_filter())
        layout.addWidget(self._create_table())
        if self.add_btn:
            layout.addWidget(
                self.add_btn,
                alignment=Qt.AlignmentFlag.AlignLeft
            )
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel(self.title)
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        lbl.setFont(QFont("Cairo", 18, QFont.Bold))
        header.addWidget(lbl)
        return header

    def _create_search_filter(self):
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("بحث ...")
        self.search_box.setMinimumWidth(200)
        search_layout = QHBoxLayout()
        search_layout.addWidget(self.search_box)

        if self.filter_items:
            self.filter_combo = QComboBox()
            self.filter_combo.addItem("الكل")
            self.filter_combo.addItems(self.filter_items)
            search_layout.addWidget(self.filter_combo)
        else:
            self.filter_combo = None

        search_layout.addStretch()
        return search_layout

    def _create_table(self):
        self.table = QTableWidget(len(self.data), len(self.columns))
        self.table.setHorizontalHeaderLabels(self.columns)
        self.table.horizontalHeader().setDefaultAlignment(
            Qt.AlignmentFlag.AlignRight
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self._fill_table(self.data)

        self.search_box.textChanged.connect(self._filter_table)
        if self.filter_combo:
            self.filter_combo.currentIndexChanged.connect(self._filter_table)

        return self.table

    def _fill_table(self, rows):
        self.table.setRowCount(len(rows))
        for row, row_data in enumerate(rows):
            for col, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                if col != len(self.columns) - 1:
                    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
                self.table.setItem(row, col, item)

    def _filter_table(self):
        txt = self.search_box.text().strip()
        filtered = []
        selected_val = self.filter_combo.currentText(
        ) if self.filter_combo else None
        for row in self.data:
            if (
                self.filter_items
                and selected_val != "الكل"
                and row[self.filter_col] != selected_val
            ):
                continue
            if txt:
                if not any(txt in str(cell) for cell in row):
                    continue
            filtered.append(row)
        self._fill_table(filtered)
