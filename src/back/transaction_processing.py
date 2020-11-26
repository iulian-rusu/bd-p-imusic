from collections import namedtuple

from src.back.db_connetcion import DBConnection
from src.back.input_processing import sanitize
from src.back.user import User


class Transaction:
    AlbumData = namedtuple("AlbumData", ['album_id', 'album_price'])
    TransactionData = namedtuple("TransactionData", ['tr_id', 'amount'])

    @staticmethod
    def make_transaction(user: User, album_id: str, amount: str, db_connection: DBConnection) -> bool:
        command = f"""
        BEGIN
            UPDATE PAYMENT_INFO SET 
                ACCOUNT_BALANCE = ACCOUNT_BALANCE - {amount} 
                WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(user.username)}');

            INSERT INTO TRANSACTIONS(USER_ID, ALBUM_ID, AMOUNT, "date") VALUES(
                (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(user.username)}'), 
                {album_id},
                {amount}, 
                SYSDATE
            );
        END;
        """
        if db_connection.exec_command(command):
            user.account_balace += int(float(amount) * 100)
            return True
        return False

    @staticmethod
    def refund_transaction(user: User, tr_id: str, amount: str, db_connection: DBConnection) -> bool:
        command = f"""
        BEGIN
            DELETE FROM TRANSACTIONS
            WHERE TR_ID={tr_id};
            
            UPDATE PAYMENT_INFO SET 
                ACCOUNT_BALANCE = ACCOUNT_BALANCE + {amount} 
                WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(user.username)}');     
        END;
        """
        if db_connection.exec_command(command):
            user.account_balace -= int(float(amount) * 100)
            return True
        return False
