from abc import ABC
from typing import Tuple

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class ArtistView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="artist name")
        self.heading(2, text="no. albums")
        self.heading(3, text="no. songs")
        self.heading(4, text="artist_id")

    def get_name_and_id(self, iid: str) -> Tuple[str, str]:
        item = self.item(iid)['values']
        return item[0], item[3]

    def load_all_rows(self, db_connection: DBConnection):
        # loads all artist data from the databases, sorted alphabetically by name
        query = '''
        SELECT 	MUSIC_ARTISTS.NAME,
                COUNT(DISTINCT MUSIC_ALBUMS.NAME),
                COUNT(SONGS.NAME),
                MUSIC_ARTISTS.ARTIST_ID
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        GROUP BY MUSIC_ARTISTS.NAME, MUSIC_ARTISTS.ARTIST_ID
        ORDER BY MUSIC_ARTISTS.NAME
        '''
        self._update_content(query, db_connection)

    def load_rows_by_name(self, name: str, db_connection: DBConnection):
        query = f'''
        SELECT 	MUSIC_ARTISTS.NAME,
                COUNT(DISTINCT MUSIC_ALBUMS.NAME),
                COUNT(SONGS.NAME),
                MUSIC_ARTISTS.ARTIST_ID
        FROM SONGS
        INNER JOIN MUSIC_ALBUMS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID = MUSIC_ARTISTS.ARTIST_ID
        WHERE LOWER(MUSIC_ARTISTS.NAME) LIKE LOWER('%{name}%')
        GROUP BY MUSIC_ARTISTS.NAME, MUSIC_ARTISTS.ARTIST_ID
        ORDER BY MUSIC_ARTISTS.NAME
        '''
        self._update_content(query, db_connection)

    def load_rows_by_parent_id(self, parent_id: str, db_connection: DBConnection):
        pass
