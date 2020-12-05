from typing import Dict

from marshmallow import Schema


class SchemaValidator:
    def __init__(self, schema: Schema):
        self._schema = schema

    def validate(self, data: Dict):
        return self._schema.validate(data)
