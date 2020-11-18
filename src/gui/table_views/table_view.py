from tkinter import ttk
import abc
from typing import Callable

from src.database.db_connetcion import DBConnection


class TableView(ttk.Treeview, metaclass=abc.ABCMeta):
    """
    Abstract base class for a table view - an object used to display table data in the GUI.
    Built on top of a ttk.Treview.
    """

    def __init__(self, *args, **kwargs):
        kwargs['show'] = 'headings'
        ttk.Treeview.__init__(self, *args, **kwargs)

    def _update_content(self, query: str, connection: DBConnection):
        cursor = connection.exec_query(query)
        if cursor:
            # query executed successfully - clear all rows and insert new ones
            self.delete(*self.get_children())
            for row in cursor:
                self.insert('', 'end', values=row)
            # free up cursor
            connection.close_cursor()

    @abc.abstractmethod
    def load_all_rows(self, connection: DBConnection):
        pass

    @abc.abstractmethod
    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        """
        Searches for matching rows and loads them into the table.

        :param key: The name of the elements to match.
        :param connection: The database connection used to run the query.
        :param parent: Optional parent name to match (like searching songs with a specified album name).
        :return: None
        """
        pass
