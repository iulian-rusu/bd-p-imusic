import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC

from src.gui.pages.base_page import BasePage
from src.gui.custom_button import CustomButton
from src.gui.table_views.albums_view import AlbumsView
from src.gui.table_views.artists_view import ArtistsView
from src.gui.table_views.songs_view import SongsView


class HomePage(BasePage, ABC):
    """
        The home page of the application.
        Contains the music catalog and allows the user to navigate to their account page.
    """

    def __init__(self, *args, **kwargs):
        BasePage.__init__(self, *args, **kwargs)
        self.build_gui()
        # default view button is songs
        self.current_view_btn = self.songs_btn
        self.on_songs_view()

    def on_back(self):
        self.master.show_page('start')

    def on_search(self):
        pass

    def on_buy(self):
        pass

    def set_current_view(self, new_btn: CustomButton):
        self.current_view_btn.config(font=BasePage.LIGHT_FONT, background='#d1d1d1')
        new_btn.config(font=BasePage.UNDERLINED_BOLD_FONT, background='#c1c1c1')
        self.current_view_btn = new_btn
        self.treeviews[self.current_view_btn].load_rows(self.master.db_connection)
        self.treeviews[self.current_view_btn].tkraise()

    def on_songs_view(self):
        self.set_current_view(self.songs_btn)
        self.buy_btn.config(state='disabled')

    def on_albums_view(self):
        self.set_current_view(self.albums_btn)
        self.buy_btn.config(state='normal')

    def on_artists_view(self):
        self.set_current_view(self.artists_btn)
        self.buy_btn.config(state='disabled')

    def on_account(self):
        pass

    def build_gui(self):
        # top menu
        self.top_menu_frame = tk.Frame(self)
        self.back_btn = CustomButton(self.top_menu_frame)
        self.back_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                             relief='flat')
        self.back_btn.config(text='back', command=self.on_back)
        self.back_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0', width='200', x='0', y='0')
        self.buy_btn = CustomButton(self.top_menu_frame)
        self.buy_btn.config(activebackground='#39a852', background='#59c872',
                            font=BasePage.LIGHT_FONT, relief='flat')
        self.buy_btn.config(state='disabled', text='buy album', command=self.on_buy)
        self.buy_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.85714', rely='0.0',
                           width='200', x='0', y='0')
        self.account_balance_lbl = ttk.Label(self.top_menu_frame)
        self.account_balance_lbl.config(background='#d1d1d1', font=BasePage.LIGHT_FONT, foreground='#515151',
                                        text='balance: $0')
        self.account_balance_lbl.place(anchor='nw', height='40', relx='0.68', width='150', x='0', y='0')
        self.search_btn = CustomButton(self.top_menu_frame)
        self.search_btn.config(activebackground='#9a9a9a', background='#c1c1c1',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.search_btn.config(text='search', command=self.on_search)
        self.search_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.142857', rely='0.0',
                              width='200', x='0', y='0')
        self.search_entry = tk.Entry(self.top_menu_frame)
        self.search_entry.config(font=BasePage.LIGHT_FONT, relief='flat')
        self.search_entry.place(anchor='nw', height='30', relx='0.3', rely='0.125', width='500', x='0', y='0')
        self.top_menu_frame.config(background='#d1d1d1', height='40', width='1400')
        self.top_menu_frame.grid()
        # bottom menu
        self.bottom_menu_frame = tk.Frame(self)
        self.songs_btn = CustomButton(self.bottom_menu_frame)
        self.songs_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                              font=BasePage.LIGHT_FONT, relief='flat')
        self.songs_btn.config(state='normal', text='songs', command=self.on_songs_view)
        self.songs_btn.place(anchor='nw', height='40', relx='0.142857', width='400', x='0', y='0')
        self.albums_btn = CustomButton(self.bottom_menu_frame)
        self.albums_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.albums_btn.config(text='albums', command=self.on_albums_view)
        self.albums_btn.place(anchor='nw', height='40', relx='0.42857', width='400', x='0', y='0')
        self.artists_btn = CustomButton(self.bottom_menu_frame)
        self.artists_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                font=BasePage.LIGHT_FONT, relief='flat')
        self.artists_btn.config(text='artists', command=self.on_artists_view)
        self.artists_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.7142857', width='400', x='0', y='0')
        self.account_btn = CustomButton(self.bottom_menu_frame)
        self.account_btn.config(activebackground='#9a9a9a', background='#b1b1b1',
                                font=BasePage.LIGHT_FONT, relief='flat')
        self.account_btn.config(text='my account', command=self.on_account)
        self.account_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                               width='200', x='0', y='0')
        self.bottom_menu_frame.config(background='#c1c1c1', height='40', width='1400')
        self.bottom_menu_frame.grid(column='0', row='2')
        self.config(height='600', width='1400')
        # table content
        self.content_frame = tk.Frame(self)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Bahnschrift Light', 12))
        self.treeviews = {
            self.songs_btn: SongsView(self.content_frame),
            self.albums_btn: AlbumsView(self.content_frame),
            self.artists_btn: ArtistsView(self.content_frame)
        }
        for view in self.treeviews.values():
            view.place(anchor='nw', height='592', width='1400', x='0', y='0')
        self.treeviews[self.songs_btn].tkraise()
        self.content_frame.config(height='592', width='1400')
        self.content_frame.grid(column='0', row='1')
