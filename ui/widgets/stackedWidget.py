from PyQt5.QtWidgets import QStackedWidget

from utils.stackedManager import StackedManager
from utils.signals import pages_signal


class StackedWidget:
    """
    Manages the creation and population of a QStackedWidget.
    """

    def __init__(self, main_window):
        """
        Initializes the StackedWidget object.

        Args:
            main_window (MainWindow): Reference to the main application window.
        """
        self.main_window = main_window
        self.clock = main_window.lbl_clock
        self.user_name = main_window.lbl_username
        self.data = main_window.data
        self.pages_number = {}
        self.stack = QStackedWidget()

    def create_stacked_widget(self):
        """
        Creates the QStackedWidget and populates it with pages.

        Returns:
            QStackedWidget: The created and populated QStackedWidget.
        """
        self._add_pages_to_stack(self.stack)
        return self.stack

    def _add_pages_to_stack(self, stack):
        """
        Adds the various pages (widgets) to the QStackedWidget.

        Args:
            stack (QStackedWidget): The QStackedWidget to add the pages to.
        """
        from ui.pages.purchase import AddPurchaseWidget, PurchasesWidget
        from ui.pages.supplier import SuppliersWidget, AddSupplierWidget
        from ui.pages.customers import AddCustomerWidget, CustomersWidget
        from ui.pages.dashboard import DashboardWidget
        from ui.pages.inventory import (
            InventoryWidget,
            StocktakingWidget,
            AddStocktakingWidget,
            AddProductWidget,
        )
        from ui.pages.reports import (
            AddReportWidget,
            ReportsWidget,
            QuickReportWidget
        )
        from ui.pages.sales import (
            AddDebtWidget,
            DebtsWidget,
            SalesWidget,
            AddSaleWidget,
        )
        from ui.pages.settings import (
            BackupWidget,
            EditUserWidget,
            SettingsWidget
        )
        from ui.widgets.tableWidget import TableWidget

        pages = [
            DashboardWidget(
                stack,
                self.clock,
                self.data["sales_today"],
                TableWidget
            ),
            SalesWidget(
                stack,
                self.data["sales_today"],
                TableWidget
            ),
            PurchasesWidget(
                stack,
                self.data["purchases"],
                TableWidget
            ),
            InventoryWidget(
                stack,
                self.data["products"],
                TableWidget
            ),
            StocktakingWidget(
                stack,
                self.data["stocktaking_data"],
                TableWidget
            ),
            DebtsWidget(
                stack,
                self.data["debts"],
                TableWidget
            ),
            CustomersWidget(
                stack,
                self.data["customers"],
                TableWidget
            ),
            SuppliersWidget(
                stack,
                self.data["suppliers"],
                TableWidget
            ),
            ReportsWidget(stack),
            SettingsWidget(stack,),
            BackupWidget(stack),
            EditUserWidget(
                stack,
                self.data["username"],
                self.data["user_phone"],
                self.user_name
            ),
            AddSaleWidget(
                stack,
                self.data["products"]
            ),
            AddSupplierWidget(
                stack,
                self.data["suppliers"]
            ),
            AddCustomerWidget(
                stack,
                self.data["customers"]
            ),
            AddStocktakingWidget(
                stack,
                self.data["stocktaking_data"]
            ),
            AddReportWidget(
                stack,
                self.data["reports"]
            ),
            QuickReportWidget(stack),
            AddProductWidget(
                stack,
                self.data["products"]
            ),
            AddDebtWidget(
                stack,
                self.data["debts"]
            ),
            AddPurchaseWidget(
                stack,
                self.data["products"],
                self.data["suppliers"],
                self.data["purchases"],
            ),
        ]

        i = 0
        for page in pages:
            stack.addWidget(page)
            page_name = str(page).split()[0].split(".")[3]
            self.pages_number[page_name] = i
            i += 1

        StackedManager().set_pages(self.pages_number)
        pages_signal.pages_ready.emit()  # send signal to refresh pages
