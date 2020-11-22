from src.back.db_connetcion import DBConnection
from src.back.input_processing import sanitize


class Transaction:
    @staticmethod
    def make_transaction(username: str, album_id: str, price: str,  connection: DBConnection) -> bool:
        command = f"""
        BEGIN
            UPDATE PAYMENT_INFO SET 
                ACCOUNT_BALANCE = ACCOUNT_BALANCE - {price} 
                WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(username)}');

            INSERT INTO TRANSACTIONS(USER_ID, ALBUM_ID, AMOUNT, "date") VALUES(
                (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(username)}'), 
                (SELECT ALBUM_ID FROM MUSIC_ALBUMS 
                INNER JOIN MUSIC_ARTISTS ON MUSIC_ALBUMS.ARTIST_ID=MUSIC_ARTISTS.ARTIST_ID
                WHERE MUSIC_ALBUMS.ALBUM_ID={album_id}),
                {price}, 
                SYSDATE
            );
        END;
        """
        return connection.exec_command(command)

    @staticmethod
    def refund_transaction(username: str, tr_id: str, price: str, db_connection: DBConnection) -> bool:
        command = f"""
        BEGIN
            DELETE FROM TRANSACTIONS
            WHERE TR_ID={tr_id};
            
            UPDATE PAYMENT_INFO SET 
                ACCOUNT_BALANCE = ACCOUNT_BALANCE + {price} 
                WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(username)}');     
        END;
        """
        return db_connection.exec_command(command)

