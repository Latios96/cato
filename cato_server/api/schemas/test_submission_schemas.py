# submission info
# config
# test suite
# tests
from marshmallow import Schema, EXCLUDE, fields
from marshmallow.validate import Length

from cato_server.api.schemas.general import (
    ID_FIELD,
    FILE_PATH_FIELD,
    NAME_FIELD,
    OPTIONAL_VARIABLES_FIELD,
)


class TestSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name: NAME_FIELD
    command: fields.String(required=True, validate=[fields.Length(min=1)])
    variables: OPTIONAL_VARIABLES_FIELD


class TestSuiteSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=[Length(min=1)])
    tests = fields.List(fields.Nested(TestSchema), required=True)
    variables = OPTIONAL_VARIABLES_FIELD


class ConfigSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    project_name = NAME_FIELD
    suites = fields.List(fields.Nested(TestSuiteSchema), required=True)
    variables = OPTIONAL_VARIABLES_FIELD


class SubmissionInfoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    config = fields.Nested(ConfigSchema, required=True)
    run_id = ID_FIELD
    resource_path = FILE_PATH_FIELD
    executable = FILE_PATH_FIELD
