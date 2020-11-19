from abc import ABC

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class SongView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="song name")
        self.heading(2, text="artist")
        self.heading(3, text="album")
        self.heading(4, text="release date")
        self.heading(5, text="genre")

    def load_all_rows(self, connection: DBConnection):
        # loads all song data from the databases, sorted alphabetically by name
        query = '''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
            MUSIC_GENRES.NAME
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        ORDER BY SONGS.NAME
        '''
        self._update_content(query, connection)

    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        query = f'''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
            MUSIC_GENRES.NAME
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        WHERE LOWER(SONGS.NAME) LIKE LOWER('%{key}%') AND LOWER(MUSIC_ALBUMS.NAME) LIKE LOWER('%{parent}%')
        ORDER BY SONGS.NAME
        '''
        self._update_content(query, connection)
