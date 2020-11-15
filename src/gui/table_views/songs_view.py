from abc import ABC

from src.gui.table_views.table_view import TableView
from src.sql.db_connetcion import DBConnection


class SongsView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="song name")
        self.heading(2, text="artist")
        self.heading(3, text="album")
        self.heading(4, text="release date")
        self.heading(5, text="genre")

    def load_rows(self, connection: DBConnection):
        # loads all song data from the databases, sorted alphabetically by name
        query = '''
        SELECT SONGS.NAME, 
            MUSIC_ARTISTS.NAME,
            MUSIC_ALBUMS.NAME, 
            TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'yyyy-mm-dd'),
            MUSIC_GENRES.NAME
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        INNER JOIN MUSIC_GENRES ON MUSIC_GENRES.GENRE_ID = SONGS.GENRE_ID 
        ORDER BY SONGS.NAME
        '''
        self._update_content(query, connection)

    def search_rows(self, key: str, cursor):
        pass
