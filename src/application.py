import logging
import tkinter as tk

from src.back.db_connetcion import DBConnection
from src.back.user import User
from src.front.pages.account_page import AccountPage
from src.front.pages.home_page import HomePage
from src.front.pages.start_page import StartPage


# test users: (test, password123), (test2, password123)


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
            logging.error(f"Unknown page: '{e}'")

    def log_in_user(self, username: str, password: str) -> bool:
        self.user = User.log_in(username, password, db_connection=self.db_connection)
        return self.user is not None

    def register_user(self, user_to_register: User) -> bool:
        flag = user_to_register.register(self.db_connection)
        if flag:
            self.user = user_to_register
        return flag

    def update_user(self, username: str, first_name: str, last_name: str, email: str, password: str) -> bool:
        return self.user.update_personal_data(username, first_name, last_name, email, password,
                                              db_connection=self.db_connection)

    def add_user_funds(self, amount_to_add: float) -> bool:
        return self.user.add_funds(amount_to_add, db_connection=self.db_connection)
