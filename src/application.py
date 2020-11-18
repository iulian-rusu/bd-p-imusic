import logging
import tkinter as tk

from src.database.db_connetcion import DBConnection
from src.gui.pages.account_page import AccountPage
from src.gui.pages.home_page import HomePage
from src.gui.pages.start_page import StartPage


class Application(tk.Tk):
    """
        Top level view of the application.
        Contains and displays GUI pages. Handles database connection and user information.
    """

    def __init__(self, db_connection: DBConnection, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db_connection = db_connection
        # dcitionary with all app pages
        self.pages = {
            'start': StartPage(title='Welcome to iMusic', master=self),
            'home': HomePage(title='Home', master=self),
            'account': AccountPage(title='My Account', master=self)
        }
        self.active_page = None
        self.user = None
        self.resizable(False, False)
        self.show_page('start')

    def show_page(self, frame_name: str):
        # sets the specified page as the current active page
        try:
            # change current active page
            self.active_page = self.pages[frame_name]
            # change window title
            self.title(self.active_page.title)
            # reset necessary widgets in the current active page
            self.active_page.reset()
            # raise the current page to the top of the screen
            self.active_page.tkraise()
        except KeyError as e:
            logging.error(f"Unknown page: {e}")
