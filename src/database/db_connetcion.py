from typing import Optional

import cx_Oracle
import logging


class DBConnection:
    """
    Provides a connection with the Oracle database.
    Handles any databases errors.
    """

    def __init__(self, host: str, port: str, service: str = ''):
        self.host = host
        self.port = port
        self.service = service
        self.dsn_tns = cx_Oracle.makedsn(self.host, self.port, service_name=self.service)
        self.connection = None
        self.cursor = None
        self.is_connected = False

    def connect(self, user: str, password: str):
        try:
            self.connection = cx_Oracle.connect(user=user, password=password, dsn=self.dsn_tns)
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

    def exec_query(self, query: str) -> Optional[cx_Oracle.Cursor]:
        if self.is_connected:
            try:
                self.cursor = self.connection.cursor()
                self.cursor.execute(query)
                logging.info("Successfully executed query")
                return self.cursor
            except cx_Oracle.Error as err:
                logging.error(f"Database error: {err}")
        return None

    def close_cursor(self):
        try:
            self.cursor.close()
        except cx_Oracle.Error as err:
            logging.error(f"Database error: {err}")

