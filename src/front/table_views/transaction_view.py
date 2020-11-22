from abc import ABC
from typing import Optional, Tuple

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class TransactionView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="album name")
        self.heading(2, text="no. songs")
        self.heading(3, text="purchased on")
        self.heading(4, text="purchased for")
        self.heading(5, text="tr_id")
        self['displaycolumns'] = self['columns'][:-1]

    def get_selected_album_data(self, event) -> Optional[Tuple[str, str]]:
        album_iid = self.identify_row(event.y)
        if album_iid != '':
            album_data = self.item(album_iid)['values']
            tr_id, album_price = album_data[4], album_data[3]
            return tr_id, album_price.lstrip('$ ')
        return None

    def load_all_rows(self, connection: DBConnection):
        # loads all transactions from database, sorted from latest to oldest
        query = f'''
        SELECT	MUSIC_ALBUMS.NAME ,
                COUNT(SONGS.SONG_ID), 
                TO_CHAR(TRANSACTIONS."date", 'dd Mon yyyy HH24:MI:SS'),
                '$'||TRANSACTIONS.AMOUNT,
                TRANSACTIONS.TR_ID
        FROM TRANSACTIONS
        INNER JOIN USERS ON TRANSACTIONS.USER_ID = USERS.USER_ID
        INNER JOIN MUSIC_ALBUMS ON TRANSACTIONS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        GROUP BY MUSIC_ALBUMS.NAME, TRANSACTIONS."date", TRANSACTIONS.AMOUNT, TRANSACTIONS.TR_ID
        ORDER BY TRANSACTIONS."date" DESC
        '''
        self._update_content(query, connection)

    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        # loads all transactions from database by a specific user, sorted from latest to oldest
        query = f'''
        SELECT	MUSIC_ALBUMS.NAME ,
                COUNT(SONGS.SONG_ID),
                TO_CHAR(TRANSACTIONS."date", 'dd Mon yyyy HH24:MI:SS'),
                '$'||TRANSACTIONS.AMOUNT,
                TRANSACTIONS.TR_ID
        FROM TRANSACTIONS
        INNER JOIN USERS ON TRANSACTIONS.USER_ID = USERS.USER_ID
        INNER JOIN MUSIC_ALBUMS ON TRANSACTIONS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        WHERE USERS.USERNAME='{key}' 
        GROUP BY MUSIC_ALBUMS.NAME, TRANSACTIONS."date", TRANSACTIONS.AMOUNT, TRANSACTIONS.TR_ID
        ORDER BY TRANSACTIONS."date" DESC
        '''
        self._update_content(query, connection)
