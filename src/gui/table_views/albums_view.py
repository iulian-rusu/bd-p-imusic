from abc import ABC

from src.gui.table_views.table_view import TableView
from src.sql.db_connetcion import DBConnection


class AlbumsView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="name")
        self.heading(2, text="price")
        self.heading(3, text="artist")
        self.heading(4, text="no. songs")
        self.heading(5, text="release date")

    def load_rows(self, connection: DBConnection):
        # loads all album data from the databases, sorted alphabetically by name
        query = '''
        SELECT	MUSIC_ALBUMS.NAME,
                '$'||MUSIC_ALBUMS.PRICE,
                MUSIC_ARTISTS.NAME,
                COUNT(SONGS.SONG_ID),
                TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'yyyy-mm-dd')
        FROM MUSIC_ALBUMS
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ARTISTS.ARTIST_ID = MUSIC_ALBUMS.ARTIST_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        GROUP BY MUSIC_ALBUMS.NAME, MUSIC_ARTISTS.NAME, MUSIC_ALBUMS.RELEASE_DATE, MUSIC_ALBUMS.PRICE
        '''
        self._update_content(query, connection)

    def search_rows(self, key: str, cursor):
        pass
