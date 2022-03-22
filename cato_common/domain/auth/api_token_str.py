import json
from base64 import b64decode
from typing import Union

from cato_common.domain.auth.bearer_token import BearerToken


class ApiTokenStr:
    def __init__(self, value: Union[bytes, str]):
        if isinstance(value, str):
            value = value.encode("utf-8")
        value = value.strip()
        if not value:
            raise ValueError("An ApiTokenStr can not be empty or blank.")
        self._value = value

    @staticmethod
    def from_bearer(bearer):
        # type: (BearerToken)->ApiTokenStr
        return ApiTokenStr(bearer.bearer_value)

    def __repr__(self):
        return str(self._value)

    def __str__(self):
        return str(self._value.decode("utf-8"))

    def __bytes__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)

    def data_dict(self):
        return json.loads(self.data_str())

    def data_str(self):
        return b64decode(self._value.split(b".")[0])

    def to_bearer(self) -> BearerToken:
        return BearerToken(self._value)
