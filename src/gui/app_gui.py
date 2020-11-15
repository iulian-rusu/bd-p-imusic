import tkinter as tk
import logging

from src.gui.pages.home_page import HomePage
from src.gui.pages.start_page import StartPage
from src.sql.db_connetcion import DBConnection


class AppGUI(tk.Frame):
    """
        Top-level view of the Grafical User Interface of the application.
        Contains all application pages and allows the selection of the current page.
    """

    def __init__(self, db_connection: DBConnection, *args, **kwargs, ):
        tk.Frame.__init__(self, *args, **kwargs)
        self.pack(side="top", fill="both", expand=True)
        # connection to database
        self.db_connection = db_connection
        # dcitionary with all app pages
        self.pages = {
            'start': StartPage(title='Welcome to iMusic', master=self),
            'home': HomePage(title='Home', master=self)
        }
        self.active_page = None
        self.master.resizable(False, False)
        self.show_page('start')

    def show_page(self, frame_name: str):
        # sets the specified page as the current active page
        try:
            self.active_page = self.pages[frame_name]
            self.active_page.show()
        except KeyError as e:
            logging.error(f"Unknown page: {e}")