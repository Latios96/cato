import humanfriendly
from marshmallow import Schema, fields, ValidationError, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato_server.domain.test_identifier import TestIdentifier
from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.api.schemas.general import (
    MachineInfoSchema,
    ID_FIELD,
    NAME_FIELD,
    VARIABLES_FIELD,
)


def is_test_identifier(string):
    try:
        TestIdentifier.from_string(string)
    except ValueError:
        raise ValidationError(f'String "{string}" is not a valid TestIdentifier.')


class CreateTestResultSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    suite_result_id = ID_FIELD
    test_name = NAME_FIELD
    test_identifier = fields.String(
        required=True, validate=[Length(min=1), is_test_identifier]
    )
    test_command = fields.String(required=True, validate=[Length(1)])
    test_variables = VARIABLES_FIELD
    machine_info = fields.Nested(MachineInfoSchema, required=True)
    execution_status = EnumField(ExecutionStatus, required=True)
    status = EnumField(TestStatus)
    output = fields.List(fields.String())
    seconds = fields.Float(min=1)
    message = fields.String(validate=[Length(1)])
    image_output = fields.Integer()
    reference_image = fields.Integer()
    started_at = fields.DateTime()
    finished_at = fields.DateTime()


class UpdateTestResultSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    execution_status = EnumField(ExecutionStatus)
    status = EnumField(TestStatus)
    output = fields.List(fields.String())
    seconds = fields.Float(min=1)
    message = fields.String(validate=[Length(1)])
    image_output = fields.Integer()
    reference_image = fields.Integer()
    started_at = fields.DateTime()
    finished_at = fields.DateTime()


class CreateOutputSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    test_result_id = ID_FIELD
    text = fields.String(
        required=True,
        allow_none=False,
        validate=[Length(max=humanfriendly.parse_size("10mb"))],
    )


class FinishTestResultSchema(Schema):
    id = ID_FIELD
    status = EnumField(TestStatus, required=True)
    seconds = fields.Float(min=0, required=True)
    message = fields.String(validate=[Length(0)], required=True)
    image_output = fields.Integer(required=False, allow_none=True)
    reference_image = fields.Integer(required=False, allow_none=True)
