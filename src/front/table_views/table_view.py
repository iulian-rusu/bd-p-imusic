from tkinter import ttk
import abc
from typing import Tuple

from src.back.db_connetcion import DBConnection


class TableView(ttk.Treeview, metaclass=abc.ABCMeta):
    """
    Abstract base class for a table view - an object used to display table data in the GUI.
    Built on top of a ttk.Treview.
    """

    def __init__(self, *args, **kwargs):
        kwargs['show'] = 'headings'
        ttk.Treeview.__init__(self, *args, **kwargs)
        # last column is the id -> hide it
        self['displaycolumns'] = self['columns'][:-1]

    def _update_content(self, query: str, db_connection: DBConnection):
        self.delete(*self.get_children())
        cursor = db_connection.fetch_data(query)
        if cursor:
            for row in cursor:
                self.insert('', 'end', values=row)
            db_connection.close_cursor()

    def reset(self):
        pass

    @abc.abstractmethod
    def get_name_and_id(self, iid: str) -> Tuple[str, str]:
        pass

    @abc.abstractmethod
    def load_all_rows(self, db_connection: DBConnection):
        pass

    @abc.abstractmethod
    def load_rows_by_name(self, name: str, db_connection: DBConnection):
        """
        Searches for matching rows and loads them into the table.

        :param name: The name of the elements to match.
        :param db_connection: The database connection used to run the query.
        :return: None
        """
        pass

    @abc.abstractmethod
    def load_rows_by_parent_id(self, parent_id: str, db_connection: DBConnection):
        """
        Searches for rows whose parent matches the given id.

        :param parent_id: The id of the parent to match
        :param db_connection: The database connection used to run the query.
        :return: None
        """
        pass
