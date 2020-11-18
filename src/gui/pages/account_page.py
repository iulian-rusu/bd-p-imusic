import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC

from src.gui.pages.base_page import BasePage
from src.gui.custom_button import CustomButton


class AccountPage(BasePage, ABC):
    """
    The user account page of the application.
    Contains the user's personal information and all purhcased music albums.
    """

    def __init__(self, *args, **kwargs):
        BasePage.__init__(self, *args, **kwargs)
        self.build_gui()
        # default view button is songs
        self.current_view_btn = None

    def reset(self):
        super().reset()
        self.on_personal_info_view()

    def on_log_out(self):
        # TODO: log current user out
        self.master.show_page('start')

    def set_current_view(self, new_btn: CustomButton):
        if self.current_view_btn:
            self.current_view_btn.config(font=BasePage.LIGHT_FONT, background='#d1d1d1')
        new_btn.config(font=BasePage.UNDERLINED_BOLD_FONT, background='#c1c1c1')
        self.current_view_btn = new_btn
        # TODO: change current view to display necessary data

    def on_home(self):
        self.master.show_page('home')

    def on_add_funds(self):
        # TODO: add more money to user's account
        pass

    def on_my_albums_view(self):
        self.set_current_view(self.my_albums_btn)

    def on_personal_info_view(self):
        self.set_current_view(self.personal_info_btn)

    def build_gui(self):
        # top menu
        self.top_menu_frame = tk.Frame(self)
        self.log_out_btn = CustomButton(self.top_menu_frame)
        self.log_out_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                                relief='flat')
        self.log_out_btn.config(text='log out', command=self.on_log_out)
        self.log_out_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                               width='200', x='0', y='0')
        self.add_funds_btn = CustomButton(self.top_menu_frame)
        self.add_funds_btn.config(activebackground='#39a852', background='#59c872',
                                  font=BasePage.LIGHT_FONT, relief='flat')
        self.add_funds_btn.config(text='add funds', command=self.on_add_funds)
        self.add_funds_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.85714', rely='0.0',
                                 width='200', x='0', y='0')
        self.account_balance_lbl = ttk.Label(self.top_menu_frame)
        self.account_balance_lbl.config(background='#d1d1d1', font=BasePage.LIGHT_FONT, foreground='#515151',
                                        text='balance: $0')
        self.account_balance_lbl.place(anchor='nw', height='40', relx='0.68', width='150', x='0', y='0')
        self.search_btn = CustomButton(self.top_menu_frame)
        self.search_btn.config(activebackground='#9a9a9a', background='#c1c1c1',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.top_menu_frame.config(background='#d1d1d1', height='40', width='1400')
        self.top_menu_frame.grid()
        # bottom menu
        self.bottom_menu_frame = tk.Frame(self)
        self.personal_info_btn = CustomButton(self.bottom_menu_frame)
        self.personal_info_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                      font=BasePage.LIGHT_FONT, relief='flat')
        self.personal_info_btn.config(state='normal', text='personal info', command=self.on_personal_info_view)
        self.personal_info_btn.place(anchor='nw', height='40', relx='0.142857', width='600', x='0', y='0')
        self.my_albums_btn = CustomButton(self.bottom_menu_frame)
        self.my_albums_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                  font=BasePage.LIGHT_FONT, relief='flat')
        self.my_albums_btn.config(text='my albums', command=self.on_my_albums_view)
        self.my_albums_btn.place(anchor='nw', height='40', relx='0.57142857', width='600', x='0', y='0')
        self.artists_btn = CustomButton(self.bottom_menu_frame)
        self.artists_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                font=BasePage.LIGHT_FONT, relief='flat')
        self.home_btn = CustomButton(self.bottom_menu_frame)
        self.home_btn.config(activebackground='#9a9a9a', background='#b1b1b1',
                             font=BasePage.LIGHT_FONT, relief='flat')
        self.home_btn.config(text='home', command=self.on_home)
        self.home_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                            width='200', x='0', y='0')
        self.bottom_menu_frame.config(background='#c1c1c1', height='40', width='1400')
        self.bottom_menu_frame.grid(column='0', row='2')
        # table content
        self.content_frame = tk.Frame(self)
        self.content_frame.config(height='591', width='1400')
        self.content_frame.grid(column='0', row='1')
