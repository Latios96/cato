from marshmallow import Schema, fields
from marshmallow.validate import Length

from cato_server.api.schemas.general import REGEX_VALID_NAME
from cato_server.api.validators.basic import SchemaValidator


class TestSchema(Schema):
    name = fields.Str(required=True, validate=[Length(min=1), REGEX_VALID_NAME])


class TestSchemaValidator:
    def test_should_validate_no_errors(self):
        schema_validator = SchemaValidator(TestSchema())

        errors = schema_validator.validate({"name": "test"})

        assert errors == {}

    def test_should_validate_with_errors(self):
        schema_validator = SchemaValidator(TestSchema())

        errors = schema_validator.validate({"name": "$test"})

        assert errors == {"name": ["String does not match expected pattern."]}
