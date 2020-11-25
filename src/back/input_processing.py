import abc
from pbkdf2 import PBKDF2

SPECIAL_CHARS = {
    '\'': '\'\'',
    '%': '\\%',
    '_': '\\_'
}


def sanitize(user_input: str) -> str:
    return ''.join(map(lambda char: SPECIAL_CHARS.get(char, char), str(user_input)))


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
    __HASH_ITERS = 1000

    @staticmethod
    def get_hash(password: str) -> str:
        salt = ''.join(map(KeyDerivator.__map_char, KeyDerivator.__SALT_PREFIX + password))
        return PBKDF2(password, salt, iterations=KeyDerivator.__HASH_ITERS).read(KeyDerivator.__HASH_LEN).hex()

    @staticmethod
    def __map_char(char: chr) -> chr:
        return chr(KeyDerivator.__SALT_OFFSET + int(ord(char) ** KeyDerivator.__SALT_POW) % KeyDerivator.__SALT_MOD)
