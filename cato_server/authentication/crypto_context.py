from passlib.context import CryptContext


class CryptoContext:
    def __init__(self):
        self._crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash_password(self, password: str) -> str:
        return self._crypt_context.hash(password)
