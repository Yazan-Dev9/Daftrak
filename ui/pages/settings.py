from PyQt5.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QFileDialog,
)
from PyQt5.QtCore import Qt

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class SettingsWidget(QWidget):

    def __init__(self, stack, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack

        # self.backup_page = backup_page
        # self.edit_user_page = edit_user_page
        self.setup_ui()

    def refresh_pages(self):
        self.backup_page = StackedManager().get_page_index("BackupWidget")
        self.edit_user_page = StackedManager().get_page_index("EditUserWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_buttons())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("الإعدادات")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignLeft)
        header.addWidget(lbl)
        return header

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_backup = QPushButton("نسخ احتياطي")
        btn_backup.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.backup_page)
        )
        btn_edit_user = QPushButton("تغيير معلومات المستخدم")
        btn_edit_user.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.edit_user_page)
        )
        btns.addWidget(btn_backup)
        btns.addWidget(btn_edit_user)
        return btns


class BackupWidget(QWidget):
    def __init__(self, stack, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.setup_ui()

    def refresh_pages(self):
        self.settings_page = StackedManager().get_page_index("SettingsWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_backup_button())
        layout.addWidget(self._create_result_label())
        layout.addLayout(self._create_back_button())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("إعدادات النسخ الاحتياطي")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_backup_button(self):
        btns = QVBoxLayout()
        self.btn_backup = QPushButton("حفظ نسخة احتياطية الآن")
        self.btn_backup.clicked.connect(self.do_backup)
        btns.addWidget(self.btn_backup)
        return btns

    def _create_result_label(self):
        self.lbl_result = QLabel("")
        return self.lbl_result

    def _create_back_button(self):
        btns = QVBoxLayout()
        btn_back = QPushButton("رجوع")
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.settings_page)
        )
        btns.addWidget(btn_back)
        return btns

    def do_backup(self):
        fname, _ = QFileDialog.getSaveFileName(
            self, "اختر مكان حفظ النسخة", "", "ملف بيانات (*.bak)"
        )
        if fname:
            # هنا تضع كود النسخ الاحتياطي الفعلي إذا أردت
            self.lbl_result.setText(f"تم حفظ النسخة الاحتياطية في: {fname}")


class EditUserWidget(QWidget):
    def __init__(self, stack, username, userphone, lbl_user, parent=None):
        super().__init__(parent)
        pages_signal.pages_ready.connect(self.refresh_pages)
        self.stack = stack
        self.username = username
        self.userphone = userphone
        self.lbl_user = lbl_user  # لعرض اسم المستخدم في مكان آخر
        self.setup_ui()

    def refresh_pages(self):
        self.settings_page = StackedManager().get_page_index("SettingsWidget")

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addLayout(self._create_header())
        layout.addLayout(self._create_form())
        layout.addLayout(self._create_buttons())
        layout.addStretch()
        self.setLayout(layout)

    def _create_header(self):
        header = QVBoxLayout()
        lbl = QLabel("تغيير معلومات المستخدم")
        lbl.setProperty("role", "header")
        lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
        header.addWidget(lbl)
        return header

    def _create_form(self):
        self.form = QFormLayout()
        self.username_field = QLineEdit()
        self.username_field.setText(self.username)
        self.phone_field = QLineEdit()
        self.phone_field.setText(self.userphone)
        self.form.addRow("اسم المستخدم:", self.username_field)
        self.form.addRow("رقم الجوال:", self.phone_field)
        return self.form

    def _create_buttons(self):
        btns = QVBoxLayout()
        btn_save = QPushButton("حفظ")
        btn_back = QPushButton("رجوع")
        btn_save.clicked.connect(self.save_user)
        btn_back.clicked.connect(
            lambda: self.stack.setCurrentIndex(self.settings_page)
        )
        btns.addWidget(btn_save)
        btns.addWidget(btn_back)
        return btns

    def save_user(self):
        self.username = self.username_field.text()
        self.userphone = self.phone_field.text()
        # تحديث label اسم المستخدم في الواجهة الرئيسية
        if self.lbl_user is not None:
            self.lbl_user.setText(f"👤 {self.username}")
        self.stack.setCurrentIndex(self.settings_page)
