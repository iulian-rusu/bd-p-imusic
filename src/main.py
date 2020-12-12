import logging

from src.application import Application
from src.back.db_connetcion import DBConnection
from src.back.input_processing import parse_args

logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s@%(asctime)s:\t%(message)s')


def main():
    args = parse_args()
    with DBConnection(args.host, args.port, args.service, user=args.username, password=args.password) as db_connection:
        app = Application(db_connection)
        app.mainloop()


if __name__ == '__main__':
    main()
