import argparse
import sys
import logging

from src.application import Application
from src.back.db_connetcion import DBConnection

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]@%(asctime)s: %(message)s')


def parse_args():
    parser = argparse.ArgumentParser(description='Parse parameters for database access.')
    parser.add_argument('-u', '--username')
    parser.add_argument('-p', '--password')
    parser.add_argument('--host')
    parser.add_argument('--port')
    parser.add_argument('--service')
    arguments = parser.parse_args()
    if not arguments.username or not arguments.password:
        logging.error("Username and password required to access database.")
        sys.exit(-1)
    if not arguments.host:
        arguments.host = 'localhost'
    if not arguments.port:
        arguments.port = '1521'
    if not arguments.service:
        arguments.service = ''
    return arguments


def on_closing(conn: DBConnection, wnd: Application):
    # handler for window close event - closes the database connection
    def close():
        conn.disconnect()
        wnd.destroy()

    return close


if __name__ == '__main__':
    # parse comand line arguments
    args = parse_args()
    # create database connection
    db_connection = DBConnection(host=args.host, port=args.port, service=args.service)
    db_connection.connect(user=args.username, password=args.password)
    # start the app
    app = Application(db_connection)
    app.protocol("WM_DELETE_WINDOW", on_closing(db_connection, app))
    app.mainloop()
