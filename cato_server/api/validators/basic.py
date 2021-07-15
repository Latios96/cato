from abc import ABC
from typing import Dict, List

from marshmallow import Schema


class SchemaValidator(ABC):
    def __init__(self, schema: Schema):
        self._schema = schema

    def validate(self, data: Dict) -> Dict[str, List[str]]:
        return self._schema.validate(data)

    def add_error(
        self, errors: Dict[str, List[str]], field_name: str, error_msg: str
    ) -> None:
        if errors.get(field_name):
            errors[field_name].append(error_msg)
        else:
            errors[field_name] = [error_msg]
