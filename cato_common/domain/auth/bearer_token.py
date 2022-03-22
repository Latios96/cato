from typing import Union


class BearerToken:
    def __init__(self, value: Union[str, bytes]):
        value = value.strip()
        if not value:
            raise ValueError("A BearerToken value can not be empty or blank.")
        self._value = value

    @staticmethod
    def parse_from_header(bearer_str: str):
        value = bearer_str.strip()
        if not value.startswith("Bearer "):
            raise ValueError("A BearerToken has to start with 'Bearer '")
        value = value.replace("Bearer ", "")
        if not value:
            raise ValueError("A BearerToken can not be empty or blank.")

    @property
    def value(self):
        return self._value

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return f"Bearer {self._value}"

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
