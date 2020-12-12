import abc

from pbkdf2 import PBKDF2

ESCAPED_CHARS = {
    '\'': '\'\'',
    '%': '\\%',
    '_': '\\_'
}


def sanitize(user_input: str) -> str:
    return ''.join(map(lambda char: ESCAPED_CHARS.get(char, char), str(user_input)))


def parse_args():
    import argparse
    import sys
    import logging
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


class KeyDerivator(metaclass=abc.ABCMeta):
    """
    Derives a hashed key using PBKDF2 (Password-Based Key Derivation Function 2).
    Do not change the private fields below unless u want to reset all user passwords.
    """
    __SALT_OFFSET = 64
    __SALT_POW = 3.14159
    __SALT_MOD = 173
    __SALT_PREFIX = 'bdp'
    __HASH_LEN = 32
    __HASH_ITERS = 30_000

    @staticmethod
    def get_hash(password: str) -> str:
        salt = ''.join(map(KeyDerivator.__map_char, KeyDerivator.__SALT_PREFIX + password))
        return PBKDF2(password, salt, iterations=KeyDerivator.__HASH_ITERS).read(KeyDerivator.__HASH_LEN).hex()

    @staticmethod
    def __map_char(char: chr) -> chr:
        return chr(KeyDerivator.__SALT_OFFSET + int(ord(char) ** KeyDerivator.__SALT_POW) % KeyDerivator.__SALT_MOD)
