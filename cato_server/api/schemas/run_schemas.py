from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato_server.api.schemas.general import (
    ID_FIELD,
    NAME_FIELD,
    VARIABLES_FIELD,
    MachineInfoSchema,
)
from cato_server.api.schemas.test_result_schemas import is_test_identifier
from cato_server.domain.execution_status import ExecutionStatus


class CreateRunSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    project_id = ID_FIELD
    started_at = fields.DateTime()


class TestForRunCreationSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    test_name = NAME_FIELD
    test_identifier = fields.String(
        required=True, validate=[Length(min=1), is_test_identifier]
    )
    test_command = fields.String(required=True, validate=[Length(1)])
    test_variables = VARIABLES_FIELD
    machine_info = fields.Nested(MachineInfoSchema, required=True)


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
