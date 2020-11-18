import logging
import tkinter as tk

from src.back.db_connetcion import DBConnection
from src.back.input_processing import KeyDerivator, sanitize
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
            logging.error(f"Unknown page: {e}")

    def log_in_user(self, username: str, password: str) -> bool:
        username = sanitize(username)
        # get hashed password
        password = KeyDerivator.get_hash(password)
        self.user = User.fetch_from_db(username, password, db_connection=self.db_connection)
        return self.user is not None

    def register_user(self, user_to_register: User) -> bool:
        # sanitize user input
        username, first_name, last_name, password, email, card_nr, expiration_date, account_balance, card_type \
            = [sanitize(str(attr)) for attr in user_to_register.__dict__.values()]
        # get hashed password
        password = KeyDerivator.get_hash(user_to_register.password)
        command = f"""
        BEGIN 
            INSERT INTO USERS (USERNAME, FIRST_NAME, LAST_NAME, PASSWORD, EMAIL)
            VALUES ('{username}', '{first_name}', '{last_name}', '{password}', NULLIF('{email}', 'NULL'));
    
            INSERT INTO PAYMENT_INFO(USER_ID, CARD_NR, EXPIRATION_DATE, ACCOUNT_BALANCE, CARD_TYPE_ID)
            VALUES ((SELECT USER_ID FROM USERS WHERE USERNAME='{username}'), '{card_nr}', TO_DATE('{expiration_date}', 
            'dd-mm-yyyy'), {account_balance}, (SELECT TYPE_ID FROM CARD_TYPES WHERE NAME=INITCAP('{card_type}'))); 
        END;
        """
        if not self.db_connection.exec_insertion(command):
            return False
        self.user = user_to_register
        return True
