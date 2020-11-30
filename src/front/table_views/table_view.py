from tkinter import ttk
import abc
from typing import Tuple

from src.back.db_loader import DBLoader


class TableView(ttk.Treeview, metaclass=abc.ABCMeta):
    """
    Abstract base class for a table view - an object used to display table data in the GUI.
    Built on top of a ttk.Treview.
    """

    def __init__(self, db_loader: DBLoader, *args, **kwargs):
        kwargs['show'] = 'headings'
        ttk.Treeview.__init__(self, *args, **kwargs)
        # last column is the id -> hide it
        self['displaycolumns'] = self['columns'][:-1]
        self.db_loader = db_loader

    def _update_content(self, query: str):
        self.db_loader.load_table(target=self, query=query)

    def reset(self):
        pass

    @abc.abstractmethod
    def get_name_and_id(self, iid: str) -> Tuple[str, str]:
        pass

    @abc.abstractmethod
    def load_all_rows(self):
        pass

    @abc.abstractmethod
    def load_rows_by_name(self, name: str):
        """
        Searches for matching rows and loads them into the table.

        :param name: The name of the elements to match.
        :return: None
        """
        pass

    @abc.abstractmethod
    def load_rows_by_parent_id(self, parent_id: str):
        """
        Searches for rows whose parent matches the given id.

        :param parent_id: The id of the parent to match
        :return: None
        """
        pass
