import abc
from pbkdf2 import PBKDF2


def sanitize(user_input: str) -> str:
    # escapes single quotes in user input
    return user_input.replace('\'', '\'\'')


class KeyDerivator(metaclass=abc.ABCMeta):
    """
    Derives a hashed key using PBKDF2 (Password-Based Key Derivation Function 2).
    """
    __SALT_OFFSET = 64
    __SALT_POW = 3.14159
    __SALT_MOD = 173
    __SALT_PREFIX = 'bdp'
    __HASH_LEN = 32
    __HASH_ITERS = 1000

    @staticmethod
    def get_hash(password: str) -> bytes:
        salt = ''.join(map(KeyDerivator.__map_char, KeyDerivator.__SALT_PREFIX + password))
        return PBKDF2(password, salt, iterations=KeyDerivator.__HASH_ITERS).read(KeyDerivator.__HASH_LEN)

    @staticmethod
    def __map_char(char: chr) -> chr:
        return chr(KeyDerivator.__SALT_OFFSET + int(ord(char) ** KeyDerivator.__SALT_POW) % KeyDerivator.__SALT_MOD)
