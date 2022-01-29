import secrets


class SessionId:
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("A SessionId can not be empty or blank.")
        self._value = value

    @staticmethod
    def none():
        return SessionId("000000000000")

    @staticmethod
    def generate():
        return SessionId(secrets.token_urlsafe())

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
