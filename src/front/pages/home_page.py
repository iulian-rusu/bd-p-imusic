import tkinter as tk
import tkinter.ttk as ttk
from abc import ABC

from src.back.input_processing import sanitize
from src.front.pages.base_page import BasePage
from src.front.custom_button import CustomButton
from src.front.table_views.album_view import AlbumView
from src.front.table_views.artist_view import ArtistView
from src.front.table_views.song_view import SongView
from src.front.table_views.table_view import TableView


class HomePage(BasePage, ABC):
    """
    The home page of the application.
    Contains the music catalog and allows the user to navigate to their account page.
    """

    def __init__(self, *args, **kwargs):
        BasePage.__init__(self, *args, **kwargs)
        self.build_gui()
        # default view button is songs
        self.current_view_btn = None
        self.entries += [self.search_entry]

    def on_log_out(self):
        self.master.user = None
        self.master.show_page('start')

    def on_search(self):
        user_input = sanitize(self.search_entry.get())
        self.table_views[self.current_view_btn].load_searched_rows(key=user_input, connection=self.master.db_connection)

    def on_buy(self):
        # TODO: create new transaction and update user data
        pass

    def on_album_select(self, event):
        # TODO: check if the 'buy' button should activate
        pass

    def on_album_open(self, event):
        self.set_current_view(self.songs_btn, load=False)
        self.search_entry.insert(0, 'album: ')
        self.search_by_parent(parent_view=self.table_views[self.albums_btn], event=event)

    def on_artist_open(self, event):
        self.set_current_view(self.albums_btn, load=False)
        self.search_entry.insert(0, 'artist: ')
        self.search_by_parent(parent_view=self.table_views[self.artists_btn], event=event)

    def set_current_view(self, new_btn: CustomButton, load: bool = True):
        if self.current_view_btn:
            self.current_view_btn.config(font=BasePage.LIGHT_FONT, background='#d1d1d1')
        new_btn.config(font=BasePage.UNDERLINED_BOLD_FONT, background='#c1c1c1')
        self.search_entry.delete(0, 'end')
        self.current_view_btn = new_btn
        if load:
            # load table content if necessary
            self.table_views[self.current_view_btn].load_all_rows(self.master.db_connection)
        self.table_views[self.current_view_btn].tkraise()

    def search_by_parent(self, parent_view: TableView, event):
        # get the index id of the album to be searched
        parent_iid = parent_view.identify_row(event.y)
        if parent_iid != '':
            # get the name of the album
            parent_name = parent_view.item(parent_iid)['values'][0]
            # search for songs whose parent (album) matches the name
            self.table_views[self.current_view_btn].load_searched_rows(key='', parent=parent_name,
                                                                       connection=self.master.db_connection)
            self.search_entry.insert('end', parent_name)

    def on_account(self):
        self.master.show_page('account')

    def reset(self):
        super().reset()
        self.account_balance_lbl.config(text=f"balance: ${self.master.user.account_balace/100.0}")
        self.set_current_view(self.songs_btn)

    def build_gui(self):
        # top menu
        self.top_menu_frame = tk.Frame(self)
        self.top_menu_frame.config(background='#d1d1d1', height='40', width='1400')
        self.top_menu_frame.grid()
        # 'log out' button
        self.log_out_btn = CustomButton(self.top_menu_frame)
        self.log_out_btn.config(activebackground='#9a9a9a', background='#b1b1b1', font=BasePage.LIGHT_FONT,
                                relief='flat')
        self.log_out_btn.config(text='log out', command=self.on_log_out)
        self.log_out_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                               width='200', x='0', y='0')
        # 'buy' button
        self.buy_btn = CustomButton(self.top_menu_frame)
        self.buy_btn.config(activebackground='#39a852', background='#59c872',
                            font=BasePage.LIGHT_FONT, relief='flat')
        self.buy_btn.config(state='disabled', text='buy album', command=self.on_buy)
        self.buy_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.85714', rely='0.0',
                           width='200', x='0', y='0')
        # 'search' button
        self.search_btn = CustomButton(self.top_menu_frame)
        self.search_btn.config(activebackground='#9a9a9a', background='#c1c1c1',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.search_btn.config(text='search', command=self.on_search)
        self.search_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.142857', rely='0.0',
                              width='200', x='0', y='0')
        # search entry
        self.search_entry = tk.Entry(self.top_menu_frame)
        self.search_entry.config(font=BasePage.LIGHT_FONT, relief='flat')
        self.search_entry.place(anchor='nw', height='30', relx='0.3', rely='0.125', width='500', x='0', y='0')
        self.search_entry.bind('<Return>', lambda event: self.on_search())
        # 'account balance' label
        self.account_balance_lbl = ttk.Label(self.top_menu_frame)
        self.account_balance_lbl.config(background='#d1d1d1', font=BasePage.LIGHT_FONT, foreground='#515151',
                                        text='balance: $0')
        self.account_balance_lbl.place(anchor='nw', height='40', relx='0.68', width='150', x='0', y='0')

        # bottom menu
        self.bottom_menu_frame = tk.Frame(self)
        self.bottom_menu_frame.config(background='#c1c1c1', height='40', width='1400')
        self.bottom_menu_frame.grid(column='0', row='2')
        # 'songs' view
        self.songs_btn = CustomButton(self.bottom_menu_frame)
        self.songs_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                              font=BasePage.LIGHT_FONT, relief='flat')
        self.songs_btn.config(state='normal', text='songs', command=lambda: self.set_current_view(self.songs_btn))
        self.songs_btn.place(anchor='nw', height='40', relx='0.142857', width='400', x='0', y='0')
        # 'albums' view
        self.albums_btn = CustomButton(self.bottom_menu_frame)
        self.albums_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                               font=BasePage.LIGHT_FONT, relief='flat')
        self.albums_btn.config(text='albums', command=lambda: self.set_current_view(self.albums_btn))
        self.albums_btn.place(anchor='nw', height='40', relx='0.42857', width='400', x='0', y='0')
        # 'artists' view
        self.artists_btn = CustomButton(self.bottom_menu_frame)
        self.artists_btn.config(activebackground='#9a9a9a', background='#d1d1d1',
                                font=BasePage.LIGHT_FONT, relief='flat')

        self.artists_btn.config(text='artists', command=lambda: self.set_current_view(self.artists_btn))
        self.artists_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.7142857', width='400', x='0', y='0')
        # 'account' view
        self.account_btn = CustomButton(self.bottom_menu_frame)
        self.account_btn.config(activebackground='#9a9a9a', background='#b1b1b1',
                                font=BasePage.LIGHT_FONT, relief='flat')
        self.account_btn.config(text='my account', command=self.on_account)
        self.account_btn.place(anchor='nw', height='40', relwidth='0.0', relx='0.0', rely='0.0',
                               width='200', x='0', y='0')

        # create tables
        self.content_frame = tk.Frame(self)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Bahnschrift Light', 12))
        self.table_views = {
            self.songs_btn: SongView(master=self.content_frame),
            self.albums_btn: AlbumView(master=self.content_frame),
            self.artists_btn: ArtistView(master=self.content_frame)
        }
        # add callbacks to tables
        self.table_views[self.albums_btn].bind('<Double 1>', self.on_album_open)
        self.table_views[self.artists_btn].bind('<Double 1>', self.on_artist_open)
        # place tables in frame
        for view in self.table_views.values():
            view.place(anchor='nw', height='591', width='1400', x='0', y='0')
        self.table_views[self.songs_btn].tkraise()
        self.content_frame.config(height='591', width='1400')
        self.content_frame.grid(column='0', row='1')
