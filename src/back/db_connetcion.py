from typing import Optional

import cx_Oracle
import logging


class DBConnection:
    """
    Provides a connection with the Oracle database.
    Handles any databases errors.
    """

    def __init__(self, host: str, port: str, service: str = '', user: str = '', password: str = ''):
        self.host = host
        self.port = port
        self.service = service
        self.user = user
        self.password = password
        self.dsn_tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
        self.connection = None
        self.cursor = None
        self.is_connected = False

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        if exc_type:
            logging.exception(f"{exc_type}: {exc_val} -> {exc_tb}")

    def connect(self):
        try:
            self.connection = cx_Oracle.connect(user=self.user, password=self.password, dsn=self.dsn_tns)
            self.is_connected = True
            logging.info("Connected to database")
        except cx_Oracle.Error as err:
            logging.error(f"Database error: {err}")

    def disconnect(self):
        if self.is_connected and self.connection:
            try:
                self.connection.close()
                self.is_connected = False
                logging.info("Disconnected from database")
            except cx_Oracle.Error as err:
                logging.error(f"Database error: {err}")

    def fetch_data(self, query: str) -> Optional[cx_Oracle.Cursor]:
        if self.is_connected:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                logging.info("Successfully fetched data")
                return self.cursor
            except cx_Oracle.Error as err:
                logging.error(f"Database error: {err}")
        return None

    def exec_command(self, sql_command: str) -> bool:
        response = False
        if self.is_connected:
            try:
                with self.connection.cursor() as cursor:
                    cursor.execute(sql_command)
                    logging.info("Successfully executed command")
                    self.connection.commit()
                    response = True
            except cx_Oracle.Error as err:
                logging.error(f"Database error: {err}")
        return response

    def close_cursor(self):
        try:
            self.cursor.close()
        except cx_Oracle.Error as err:
            logging.error(f"Database error: {err}")
