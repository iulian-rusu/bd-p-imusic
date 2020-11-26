from typing import Optional

from src.back.db_connetcion import DBConnection
from src.back.input_processing import sanitize, KeyDerivator


class User:
    NO_EMAIL_MSG = 'unspecified'
    MIN_PASS_LEN = 8
    MAX_PASS_LEN = 30

    def __init__(self, username: str, first_name: str, last_name: str, hashed_password: str, email: str,
                 card_nr: str, expiration_date: str, account_balance: str, card_type: str):
        # personal info
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.__hashed_password = hashed_password
        self.email = email if email else User.NO_EMAIL_MSG
        # payment info
        self.card_nr = card_nr
        self.expiration_date = expiration_date
        self.account_balace = int(float(account_balance) * 100)
        self.card_type = card_type

    def __str__(self) -> str:
        return f"USERNAME:\t{self.username}\nFIRST NAME:\t{self.first_name}\nLAST NAME:\t{self.last_name}" \
               f"\nPASSWORD:\t{self.__hashed_password}\nEMAIL:\t\t{self.email}\nCARD NR:\t{self.card_nr}" \
               f"\nEXP DATE:\t{self.expiration_date}\nBALANCE:\t${self.account_balace / 100.0}" \
               f"\nCARD TYPE:\t{self.card_type}\n"

    def has_empty_fields(self) -> bool:
        return any(map(lambda attr: len(str(attr)) == 0, vars(self).values()))

    def match_password(self, password: str) -> bool:
        return KeyDerivator.get_hash(sanitize(password)) == self.__hashed_password

    def register(self, db_connection: DBConnection) -> bool:
        username, first_name, last_name, password, email, card_nr, expiration_date, account_balance, card_type \
            = [sanitize(str(attr)) for attr in vars(self).values()]
        self.__hashed_password = KeyDerivator.get_hash(password)
        command = f"""
        BEGIN 
            INSERT INTO USERS (USERNAME, FIRST_NAME, LAST_NAME, PASSWORD, EMAIL) VALUES (
                    '{username}', 
                    '{first_name}', 
                    '{last_name}', 
                    '{self.__hashed_password}', 
                    NULLIF('{email}', '{User.NO_EMAIL_MSG}')
            );
            INSERT INTO PAYMENT_INFO(USER_ID, CARD_NR, EXPIRATION_DATE, ACCOUNT_BALANCE, CARD_TYPE_ID) VALUES (
                (SELECT USER_ID FROM USERS WHERE USERNAME='{username}'), 
                '{card_nr}',
                TO_DATE('{expiration_date}', 'dd-mm-yyyy'), 
                {account_balance}, 
                (SELECT TYPE_ID FROM CARD_TYPES WHERE NAME=INITCAP('{card_type}'))
            ); 
        END;
        """
        return db_connection.exec_command(command)

    def update_personal_data(self, username: str, first_name: str, last_name: str, email: str, password: str,
                             db_connection: DBConnection) -> bool:
        if len(password) == 0:
            password = self.__hashed_password
        else:
            password = KeyDerivator.get_hash(sanitize(password))
        command = f"""
            UPDATE USERS SET 
            USERNAME='{sanitize(username)}',
            FIRST_NAME='{sanitize(first_name)}',
            LAST_NAME='{sanitize(last_name)}',
            EMAIL=NULLIF('{sanitize(email)}','{User.NO_EMAIL_MSG}'), 
            PASSWORD='{password}' 
            WHERE USERNAME='{self.username}'
        """
        if db_connection.exec_command(command):
            self.username = username
            self.first_name = first_name
            self.last_name = last_name
            self.email = email
            self.__hashed_password = password
            return True
        return False

    def add_funds(self, amount_to_add: str, db_connection: DBConnection) -> bool:
        command = f"""
            UPDATE PAYMENT_INFO SET 
            ACCOUNT_BALANCE = ACCOUNT_BALANCE + {amount_to_add} 
            WHERE USER_ID IN (SELECT USER_ID FROM USERS WHERE USERNAME='{sanitize(self.username)}')
        """
        if db_connection.exec_command(command):
            self.account_balace += int(float(amount_to_add) * 100)
            return True
        return False

    @classmethod
    def from_login(cls, username: str, password: str, db_connection: DBConnection) -> Optional['User']:
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
        WHERE USERS.USERNAME = '{sanitize(username)}' AND USERS.PASSWORD = '{KeyDerivator.get_hash(sanitize(password))}'
        '''
        result = db_connection.fetch_data(query)
        row = result.fetchone()
        if row:
            return cls(*row)
        return None
