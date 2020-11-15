from tkinter import ttk
import abc

from src.sql.db_connetcion import DBConnection


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
        # clear all rows and insert new ones
        self.delete(*self.get_children())
        for row in cursor:
            self.insert('', 'end', values=row)
        # free up cursor
        connection.close_cursor()

    @abc.abstractmethod
    def load_rows(self, connection: DBConnection):
        pass

    @abc.abstractmethod
    def search_rows(self, key: str, cursor):
        pass
