from abc import ABC
from typing import Tuple
import tkinter.ttk as ttk

from src.front.pages.base_page import BasePage
from src.front.table_views.table_view import TableView


class SongView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5, 6)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="song name")
        self.heading(2, text="artist")
        self.heading(3, text="album")
        self.heading(4, text="release date")
        self.heading(5, text="genre", command=self.on_genre_heading_click)
        self.heading(6, text="song_id")
        # add genre combobox
        self.genre_select_cmbx = ttk.Combobox(master=self.master)
        self.genre_select_cmbx.config(state='readonly', font=BasePage.LIGHT_FONT)
        self.genre_select_cmbx.bind('<<ComboboxSelected>>', lambda event: self.on_genre_select())
        self.genre_select_cmbx.set('select genre')
        self.genres = {
            'All': 0
        }
        self.selected_genre_id = 0
        self.genre_select_callback = None

    def reset(self):
        self.selected_genre_id = 0
        self.heading(5, text="genre")

    def on_genre_heading_click(self):
        self.genre_select_cmbx.place(anchor='nw', height='25', width='280', relx='0.8', y='0')
        self.genre_select_cmbx.tkraise()

    def on_genre_select(self):
        self.tkraise()
        selected_genre = self.genre_select_cmbx.get()
        self.genre_select_cmbx.set('select genre')
        self.selected_genre_id = self.genres.get(selected_genre, 0)
        if self.selected_genre_id > 0:
            self.heading(5, text=selected_genre)
        if self.genre_select_callback:
            self.genre_select_callback(self.selected_genre_id)

    def update_genre_content(self):
        query = 'SELECT GENRE_ID, NAME FROM MUSIC_GENRES'
        self.db_loader.load_combobox(target=self, query=query)

    def get_name_and_id(self, iid: str) -> Tuple[str, str]:
        item = self.item(iid)['values']
        return item[0], item[5]

    def load_all_rows(self):
        query = '''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
            MUSIC_GENRES.NAME,
            SONGS.SONG_ID
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        ORDER BY SONGS.NAME
        '''
        self._update_content(query)

    def load_rows_by_name(self, name: str, parent: str = ''):
        query = f'''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
            MUSIC_GENRES.NAME,
            SONGS.SONG_ID
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        WHERE LOWER(SONGS.NAME) LIKE LOWER('%{name}%')
        {f'AND MUSIC_GENRES.GENRE_ID = {self.selected_genre_id}' if self.selected_genre_id > 0 else ''}
        ORDER BY SONGS.NAME
        '''
        self._update_content(query)

    def load_rows_by_parent_id(self, parent_id: str):
        query = f'''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
            MUSIC_GENRES.NAME,
            SONGS.SONG_ID
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        WHERE SONGS.ALBUM_ID = {parent_id}
        ORDER BY SONGS.NAME
        '''
        self._update_content(query)

    def load_rows_by_genre_id(self, genre_id: int):
        if genre_id == 0:
            self.load_all_rows()
        else:
            query = f'''
            SELECT SONGS.NAME, 
                MUSIC_ARTISTS.NAME,
                MUSIC_ALBUMS.NAME, 
                TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
                MUSIC_GENRES.NAME,
                SONGS.SONG_ID
            FROM SONGS
            INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
            INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
            INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
            WHERE MUSIC_GENRES.GENRE_ID = {genre_id}
            ORDER BY SONGS.NAME
            '''
            self._update_content(query)
