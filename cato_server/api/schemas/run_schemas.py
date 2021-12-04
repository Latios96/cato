from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato.domain.comparison_method import ComparisonMethod
from cato_server.api.schemas.general import (
    ID_FIELD,
    NAME_FIELD,
    VARIABLES_FIELD,
)
from cato_server.api.schemas.test_result_schemas import is_test_identifier


class ComparisonSettingsSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    method = EnumField(ComparisonMethod, required=True)
    threshold = fields.Float(min=0, required=True)


class TestForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    test_name = NAME_FIELD
    test_identifier = fields.String(
        required=True, validate=[Length(min=3), is_test_identifier]
    )
    test_command = fields.String(required=True, validate=[Length(1)])
    test_variables = VARIABLES_FIELD
    comparison_settings = fields.Nested(ComparisonSettingsSchema, required=True)


class TestSuiteForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    suite_name = NAME_FIELD
    suite_variables = VARIABLES_FIELD
    tests = fields.List(fields.Nested(TestForRunCreationSchema), required=True)


class CreateFullRunSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    project_id = ID_FIELD
    test_suites = fields.List(
        fields.Nested(TestSuiteForRunCreationSchema), required=True
    )
    branch_name = fields.String(
        validate=[Length(min=1)], required=False, allow_none=True
    )
