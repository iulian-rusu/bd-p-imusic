from src.back.db_connetcion import DBConnection
from src.back.input_processing import sanitize


class Transaction:
    @staticmethod
    def buy_album(username: str, album_name: str, price: str, artist_name: str, connection: DBConnection) -> bool:
        command = f"""
        BEGIN
            UPDATE PAYMENT_INFO SET 
            ACCOUNT_BALANCE = ACCOUNT_BALANCE - {price} 
            WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(username)}');

            INSERT INTO TRANSACTIONS(USER_ID, ALBUM_ID, AMOUNT, "date") VALUES(
                (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(username)}'), 
                (SELECT ALBUM_ID FROM MUSIC_ALBUMS 
                INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID=MUSIC_ARTISTS.ARTIST_ID
                WHERE MUSIC_ALBUMS.NAME='{sanitize(album_name)}' AND MUSIC_ARTISTS.NAME='{sanitize(artist_name)}'),
                {price}, 
                SYSDATE
            );
        END;
        """
        return connection.exec_command(command)
