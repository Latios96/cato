class SecretStr:
    def __init__(self, value):
        if not value:
            raise ValueError("A secret string can not be empty.")
        self._value = value

    def get_secret_value(self):
        return self._value

    def __repr__(self):
        return "******"

    def __str__(self):
        return "******"

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
