from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato_common.domain.comparison_method import ComparisonMethod
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

    testName = NAME_FIELD
    testIdentifier = fields.String(
        required=True, validate=[Length(min=3), is_test_identifier]
    )
    testCommand = fields.String(required=True, validate=[Length(1)])
    testVariables = VARIABLES_FIELD
    comparisonSettings = fields.Nested(ComparisonSettingsSchema, required=True)


class TestSuiteForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    suiteName = NAME_FIELD
    suiteVariables = VARIABLES_FIELD
    tests = fields.List(fields.Nested(TestForRunCreationSchema), required=True)


class CreateFullRunSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    projectId = ID_FIELD
    testSuites = fields.List(
        fields.Nested(TestSuiteForRunCreationSchema), required=True
    )
    branchName = fields.String(
        validate=[Length(min=1)], required=False, allow_none=True
    )
