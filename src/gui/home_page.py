import tkinter as tk
from abc import ABC

from src.gui.base_page import BasePage


class HomePage(BasePage, ABC):
    """
        The home page of the application.
        Contains the music catalog and allows the user to navigate to their account page.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.build_gui()

    def on_back(self):
        self.master.show_page('start')

    @staticmethod
    def get_wnd_title() -> str:
        return 'Home'

    def build_gui(self):
        # add a home label
        self.home_lbl = tk.Label(self)
        self.home_lbl.config(font=BasePage.font('12'), text='Home')
        self.home_lbl.grid(column='0', row='0', columnspan='2', padx='5', pady='10')
        # back button
        self.login_btn = tk.Button(self)
        self.login_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.font('12'), relief='flat')
        self.login_btn.config(text='back')
        self.login_btn.configure(command=self.on_back)
        self.login_btn.grid(column='0', row='1', columnspan='2', padx='5', pady='10')
