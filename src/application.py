import logging
import tkinter as tk

from src.back.db_connetcion import DBConnection
from src.back.transaction_processing import Transaction
from src.back.user import User
from src.front.pages.account_page import AccountPage
from src.front.pages.home_page import HomePage
from src.front.pages.start_page import StartPage


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
            self.active_page = self.pages[frame_name]
            self.title(self.active_page.title)
            # reset necessary widgets in the current active page
            self.active_page.reset()
            self.active_page.tkraise()
        except KeyError as e:
            logging.error(f"Unknown page: '{e}'")

    def log_in_user(self, username: str, password: str) -> bool:
        self.user = User.from_login(username, password, db_connection=self.db_connection)
        if self.user:
            logging.info(f"User '{username}' logged in")
            self.show_page('home')
            return True
        logging.info(f"Failed log in for username: '{username}'")
        return False

    def register_user(self, user_to_register: User) -> bool:
        flag = user_to_register.register(self.db_connection)
        if flag:
            self.user = user_to_register
            logging.info(f"New user registered: '{self.user.username}'")
            self.show_page('home')
        return flag

    def buy_album(self, album_id: str, price: str) -> bool:
        if Transaction.make_transaction(self.user.username, album_id, price, self.db_connection):
            self.user.account_balace -= int(float(price) * 100)
            return True
        return False

    def refund_transaction(self, tr_id: str, price: str) -> bool:
        if Transaction.refund_transaction(self.user.username, tr_id, price, self.db_connection):
            self.user.account_balace += int(float(price) * 100)
            return True
        return False

    def update_user(self, username: str, first_name: str, last_name: str, email: str, password: str) -> bool:
        return self.user.update_personal_data(username, first_name, last_name, email, password,
                                              db_connection=self.db_connection)

    def add_user_funds(self, amount_to_add: str) -> bool:
        return self.user.add_funds(amount_to_add, db_connection=self.db_connection)
