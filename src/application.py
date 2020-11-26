import logging
import tkinter as tk
from typing import Callable

from src.back.back_thread import BackThread
from src.back.db_connetcion import DBConnection
from src.back.transaction_processing import Transaction
from src.back.user import User
from src.front.pages.account_page import AccountPage
from src.front.pages.home_page import HomePage
from src.front.pages.start_page import StartPage


class Application(tk.Tk):
    """
    Top level view of the application.
    Contains objects that manage the GUI, database connection and user data.
    """

    def __init__(self, db_connection: DBConnection, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.db_connection = db_connection
        self.back_thread = BackThread()
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

    def mainloop(self, n=0):
        self.back_thread.start()
        tk.Tk.mainloop(self, n)

    def destroy(self):
        # thread commits sudoku
        self.back_thread.add_task(self.back_thread.stop)
        tk.Tk.destroy(self)

    def run_background_task(self, task: Callable):
        self.back_thread.add_task(task)

    def show_page(self, frame_name: str):
        try:
            self.active_page = self.pages[frame_name]
            self.title(self.active_page.title)
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
        has_registered = user_to_register.register(self.db_connection)
        if has_registered:
            self.user = user_to_register
            logging.info(f"New user registered: '{self.user.username}'")
            self.show_page('home')
        return has_registered

    def buy_album(self, album_id: str, album_price: str) -> bool:
        return Transaction.make_transaction(self.user, album_id, album_price, self.db_connection)

    def refund_transaction(self, tr_id: str, amount: str) -> bool:
        return Transaction.refund_transaction(self.user, tr_id, amount, self.db_connection)

    def update_user(self, username: str, first_name: str, last_name: str, email: str, password: str) -> bool:
        return self.user.update_personal_data(username, first_name, last_name, email, password,
                                              db_connection=self.db_connection)

    def add_user_funds(self, amount_to_add: str) -> bool:
        return self.user.add_funds(amount_to_add, db_connection=self.db_connection)
