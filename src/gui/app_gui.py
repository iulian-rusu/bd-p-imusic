import tkinter as tk
import logging

from src.gui.home_page import HomePage
from src.gui.start_page import StartPage

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]@%(asctime)s: %(message)s')


class AppGUI(tk.Frame):
    """
        Top-level view of the Grafical User Interface of the application.
        Contains all application pages and allows the selection of the current page.
    """
    HEIGHT = '1000'
    WIDTH = '1500'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pack(side="top", fill="both", expand=True)
        # dcitionary with all app pages
        self.pages = {
            'start': StartPage(title='Welcome to iMusic', master=self, width=AppGUI.WIDTH, height=AppGUI.HEIGHT),
            'home': HomePage(title='Home', master=self, width=AppGUI.WIDTH, height=AppGUI.HEIGHT)
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