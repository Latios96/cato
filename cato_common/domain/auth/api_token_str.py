import json
from base64 import b64decode


class ApiTokenStr:
    def __init__(self, value: bytes):
        value = value.strip()
        if not value:
            raise ValueError("An ApiTokenStr can not be empty or blank.")
        self._value = value

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return str(self._value.decode("utf-8"))

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def data_dict(self):
        return json.loads(self.data_str())

    def data_str(self):
        return b64decode(self._value.split(b".")[0])
