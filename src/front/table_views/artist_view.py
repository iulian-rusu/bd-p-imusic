from abc import ABC

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class ArtistView(TableView, ABC):

    def __init__(self,  *args, **kwargs):
        kwargs['columns'] = (1, 2, 3)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="artist name")
        self.heading(2, text="no. albums")
        self.heading(3, text="no. songs")

    def load_all_rows(self, connection: DBConnection):
        # loads all artist data from the databases, sorted alphabetically by name
        query = '''
        SELECT 	MUSIC_ARTISTS.NAME,
                COUNT(DISTINCT MUSIC_ALBUMS.NAME),
                COUNT(SONGS.NAME) 
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        GROUP BY MUSIC_ARTISTS.NAME
        ORDER BY MUSIC_ARTISTS.NAME
        '''
        self._update_content(query, connection)

    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        query = f'''
        SELECT 	MUSIC_ARTISTS.NAME,
                COUNT(DISTINCT MUSIC_ALBUMS.NAME),
                COUNT(SONGS.NAME) 
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        WHERE LOWER(MUSIC_ARTISTS.NAME) LIKE LOWER('%{key}%')
        GROUP BY MUSIC_ARTISTS.NAME
        ORDER BY MUSIC_ARTISTS.NAME
        '''
        self._update_content(query, connection)
