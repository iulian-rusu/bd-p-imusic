from abc import ABC
from typing import Optional, Tuple

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class AlbumView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5, 6)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="album name")
        self.heading(2, text="price")
        self.heading(3, text="artist")
        self.heading(4, text="no. songs")
        self.heading(5, text="release date")
        self.heading(6, text="album_id")
        self['displaycolumns'] = self['columns'][:-1]

    def get_selected_album_data(self, event) -> Optional[Tuple[str, str]]:
        album_iid = self.identify_row(event.y)
        if album_iid != '':
            album_data = self.item(album_iid)['values']
            album_id, album_price = album_data[5], album_data[1]
            return album_id, album_price.lstrip('$ ')
        return None

    def load_all_rows(self, connection: DBConnection):
        # loads all album data from the databases, sorted alphabetically by name
        query = '''
        SELECT	MUSIC_ALBUMS.NAME,
                '$'||MUSIC_ALBUMS.PRICE,
                MUSIC_ARTISTS.NAME,
                COUNT(SONGS.SONG_ID),
                TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
                MUSIC_ALBUMS.ALBUM_ID
        FROM MUSIC_ALBUMS
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ARTISTS.ARTIST_ID = MUSIC_ALBUMS.ARTIST_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        GROUP BY MUSIC_ALBUMS.NAME, MUSIC_ARTISTS.NAME, MUSIC_ALBUMS.RELEASE_DATE, MUSIC_ALBUMS.PRICE, 
        MUSIC_ALBUMS.ALBUM_ID
        ORDER BY MUSIC_ALBUMS.NAME
        '''
        self._update_content(query, connection)

    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        query = f'''
        SELECT	MUSIC_ALBUMS.NAME,
                '$'||MUSIC_ALBUMS.PRICE,
                MUSIC_ARTISTS.NAME,
                COUNT(SONGS.SONG_ID),
                TO_CHAR(MUSIC_ALBUMS.RELEASE_DATE, 'dd Mon yyyy'),
                MUSIC_ALBUMS.ALBUM_ID
        FROM MUSIC_ALBUMS
        INNER JOIN MUSIC_ARTISTS ON MUSIC_ARTISTS.ARTIST_ID = MUSIC_ALBUMS.ARTIST_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        WHERE LOWER(MUSIC_ALBUMS.NAME) LIKE LOWER('%{key}%') AND LOWER(MUSIC_ARTISTS.NAME) LIKE LOWER('%{parent}%')
        GROUP BY MUSIC_ALBUMS.NAME, MUSIC_ARTISTS.NAME, MUSIC_ALBUMS.RELEASE_DATE, MUSIC_ALBUMS.PRICE,
        MUSIC_ALBUMS.ALBUM_ID
        ORDER BY MUSIC_ALBUMS.NAME
        '''
        self._update_content(query, connection)
