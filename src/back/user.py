from typing import Optional

from src.back.db_connetcion import DBConnection


class User:
    def __init__(self, username: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 password: str = None,
                 email: str = '',
                 card_nr: str = None,
                 expiration_date: str = None,
                 account_balance: str = None,
                 card_type: str = None):
        # personal info
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.email = email
        # payment info
        self.card_nr = card_nr
        self.expiration_date = expiration_date
        self.account_balace = int(float(account_balance) * 100)
        self.card_type = card_type

    def __str__(self) -> str:
        return f"USERNAME:\t{self.username}\nFIRST NAME:\t{self.first_name}\nLAST NAME:\t{self.last_name}" \
               f"\nPASSWORD:\t{self.password}\nEMAIL:\t\t{self.email}\nCARD NR:\t{self.card_nr}" \
               f"\nEXP DATE:\t{self.expiration_date}\nBALANCE:\t${self.account_balace/100.0}" \
               f"\nCARD TYPE:\t{self.card_type}\n"

    def has_empty_fields(self) -> bool:
        return any(map(lambda attr: len(str(attr)) == 0, self.__dict__.values()))

    @staticmethod
    def fetch_from_db(username: str, password: str, db_connection: DBConnection) -> Optional['User']:
        query = f'''
        SELECT  USERS.USERNAME,
                USERS.FIRST_NAME,
                USERS.LAST_NAME, 
                USERS.PASSWORD, 
                USERS.EMAIL,
                PAYMENT_INFO.CARD_NR,
                TO_CHAR(PAYMENT_INFO.EXPIRATION_DATE, 'dd Mon yyyy'), 
                PAYMENT_INFO.ACCOUNT_BALANCE, 
                CARD_TYPES.NAME
        FROM USERS
        INNER JOIN PAYMENT_INFO ON USERS.USER_ID = PAYMENT_INFO.USER_ID
        INNER JOIN CARD_TYPES ON PAYMENT_INFO.CARD_TYPE_ID = CARD_TYPES.TYPE_ID
        WHERE USERS.USERNAME = '{username}' AND USERS.PASSWORD = '{password}'
        '''
        result = db_connection.exec_query(query)
        row = result.fetchone()
        if row:
            return User(*row)
        return None
