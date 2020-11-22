from abc import ABC

from src.front.table_views.table_view import TableView
from src.back.db_connetcion import DBConnection


class TransactionView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="album name")
        self.heading(2, text="no. songs")
        self.heading(3, text="purchased on")
        self.heading(4, text="purchased for")

    def load_all_rows(self, connection: DBConnection):
        # loads all transactions from database, sorted from latest to oldest
        query = f'''
        SELECT	MUSIC_ALBUMS.NAME ,
                COUNT(SONGS.SONG_ID), 
                TO_CHAR(TRANSACTIONS."date", 'dd Mon yyyy HH24:MI:SS'),
                '$'||TRANSACTIONS.AMOUNT
        FROM TRANSACTIONS
        INNER JOIN USERS ON TRANSACTIONS.USER_ID = USERS.USER_ID
        INNER JOIN MUSIC_ALBUMS ON TRANSACTIONS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        GROUP BY MUSIC_ALBUMS.NAME, TRANSACTIONS."date", TRANSACTIONS.AMOUNT
        ORDER BY TRANSACTIONS."date" DESC
        '''
        self._update_content(query, connection)

    def load_searched_rows(self, key: str, connection: DBConnection, parent: str = ''):
        # loads all transactions from database by a specific user, sorted from latest to oldest
        query = f'''
        SELECT	MUSIC_ALBUMS.NAME ,
                COUNT(SONGS.SONG_ID),
                TO_CHAR(TRANSACTIONS."date", 'dd Mon yyyy HH24:MI:SS'),
                '$'||TRANSACTIONS.AMOUNT
        FROM TRANSACTIONS
        INNER JOIN USERS ON TRANSACTIONS.USER_ID = USERS.USER_ID
        INNER JOIN MUSIC_ALBUMS ON TRANSACTIONS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID
        INNER JOIN SONGS ON SONGS.ALBUM_ID = MUSIC_ALBUMS.ALBUM_ID 
        WHERE USERS.USERNAME='{key}' 
        GROUP BY MUSIC_ALBUMS.NAME, TRANSACTIONS."date", TRANSACTIONS.AMOUNT
        ORDER BY TRANSACTIONS."date" DESC
        '''
        self._update_content(query, connection)
