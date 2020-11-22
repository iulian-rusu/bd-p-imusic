import argparse
import sys
import logging

from src.application import Application
from src.back.db_connetcion import DBConnection

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s]@%(asctime)s:\t%(message)s')


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


if __name__ == '__main__':
    args = parse_args()
    with DBConnection(args.host, args.port, args.service, user=args.username, password=args.password) as db_connection:
        app = Application(db_connection)
        app.mainloop()
