class StackedManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(StackedManager, cls).__new__(cls)
            cls._instance.pages = None
            cls._instance.sidebar_items = None
        return cls._instance

    def set_pages(self, pages):
        self.pages = pages

    def get_sidebar_items(self):
        return self.sidebar_items

    def set_sidebar_items(self, sidebar_items):
        self.sidebar_items = sidebar_items

    def get_page_index(self, page_name):
        """
        Retrieves the index of a page given its name.

        Args:
            page_name (str): The name of the page (widget).
            For example, 'DashboardWidget'.

        Returns:
            int: The index of the page in the stacked widget,
            or None if the page is not found.
        """
        return self.pages.get(page_name)

    def get_sidebar_index(self, item_name):
        """
        Retrieves the index of a side bar item given its name.
        Args:
            item_name (str): The name of the side bar item.
            For example, 'Dashboard'.
        Returns:
            int: The index of the side bar item,
            or None if the item is not found.
        """
        return self.sidebar_items.get(item_name)
