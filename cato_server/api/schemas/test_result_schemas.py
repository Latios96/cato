import humanfriendly
from marshmallow import Schema, fields, ValidationError, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato_common.domain.test_status import TestStatus
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_server.api.schemas.general import (
    MachineInfoSchema,
    ID_FIELD,
)


def is_test_identifier(string):
    try:
        TestIdentifier.from_string(string)
    except ValueError:
        raise ValidationError(f'String "{string}" is not a valid TestIdentifier.')


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
    diff_image = fields.Integer(required=False, allow_none=True)
    error_value = fields.Float(required=True, allow_none=True)
    failure_reason = EnumField(TestFailureReason, required=False, allow_none=True)


class StartTestResultSchema(Schema):
    id = ID_FIELD
    machine_info = fields.Nested(MachineInfoSchema, required=True)
