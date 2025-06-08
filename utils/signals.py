from PyQt5.QtCore import QObject, pyqtSignal

from PyQt5.QtWidgets import QListWidget


class PagesSignal(QObject):
    pages_ready = pyqtSignal()


class SideBarSingle(QObject):
    sidebar_ready = pyqtSignal(QListWidget)
    item_ready = pyqtSignal()


pages_signal = PagesSignal()
sidebar_signal = SideBarSingle()
