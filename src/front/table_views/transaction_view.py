import logging
from abc import ABC
from typing import Optional, Tuple

from src.front.table_views.table_view import TableView


class TransactionView(TableView, ABC):

    def __init__(self, *args, **kwargs):
        kwargs['columns'] = (1, 2, 3, 4, 5)
        TableView.__init__(self, *args, **kwargs)
        self.heading(1, text="album name")
        self.heading(2, text="no. songs")
        self.heading(3, text="purchased on")
        self.heading(4, text="purchased for")
        self.heading(5, text="tr_id")

    def get_selected_transaction_data(self, event) -> Optional[Tuple[str, str]]:
        album_iid = self.identify_row(event.y)
        if album_iid != '':
            album_data = self.item(album_iid)['values']
            tr_id, amount = album_data[4], album_data[3]
            return tr_id, amount.lstrip('$ ')
        return None

    def get_name_and_id(self, iid: str) -> Tuple[str, str]:
        item = self.item(iid)['values']
        return item[0], item[4]

    def delete_transaction_row(self, tr_id: str):
        selected_items = self.selection()
        for iid in selected_items:
            if self.item(iid)['values'][4] == tr_id:
                self.delete(iid)
                return

    def load_all_rows(self):
        logging.warning("Cannot load transactions from other users")

    def load_rows_by_name(self, name: str):
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
        WHERE USERS.USERNAME='{name}' 
        GROUP BY MUSIC_ALBUMS.NAME, TRANSACTIONS."date", TRANSACTIONS.AMOUNT, TRANSACTIONS.TR_ID
        ORDER BY TRANSACTIONS."date" DESC
        '''
        self._update_content(query)

    def load_rows_by_parent_id(self, parent_id: str):
        pass
