import secrets


class ApiTokenId:
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("An ApiTokenId can not be empty or blank.")
        self._value = value

    @staticmethod
    def generate():
        return ApiTokenId(secrets.token_hex())

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
