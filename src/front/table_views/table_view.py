from tkinter import ttk
import abc

from src.back.db_connetcion import DBConnection


class TableView(ttk.Treeview, metaclass=abc.ABCMeta):
    """
    Abstract base class for a table view - an object used to display table data in the GUI.
    Built on top of a ttk.Treview.
    """

    def __init__(self, *args, **kwargs):
        kwargs['show'] = 'headings'
        ttk.Treeview.__init__(self, *args, **kwargs)
        self['displaycolumns'] = self['columns'][:-1]

    def _update_content(self, query: str, connection: DBConnection):
        cursor = connection.fetch_data(query)
        if cursor:
            # query executed successfully - clear all rows and insert new ones
            self.delete(*self.get_children())
            for row in cursor:
                self.insert('', 'end', values=row)
            # free up cursor
            connection.close_cursor()

    @abc.abstractmethod
    def get_name_and_id(self, iid: str):
        pass

    @abc.abstractmethod
    def load_all_rows(self, connection: DBConnection):
        pass

    @abc.abstractmethod
    def load_searched_rows(self, key: str, connection: DBConnection):
        """
        Searches for matching rows and loads them into the table.

        :param key: The name of the elements to match.
        :param connection: The database connection used to run the query.
        :return: None
        """
        pass

    @abc.abstractmethod
    def load_rows_by_parent_id(self, parent_id: str, connection: DBConnection):
        """
        Searches for rows whose parent matches the given id.

        :param parent_id: The id of the parent to match
        :param connection: The database connection used to run the query.
        :return: None
        """
        pass
