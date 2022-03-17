import humanfriendly
from marshmallow import Schema, fields, ValidationError, EXCLUDE
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato_common.domain.result_status import ResultStatus
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

    testResultId = ID_FIELD
    text = fields.String(
        required=True,
        allow_none=False,
        validate=[Length(max=humanfriendly.parse_size("10mb"))],
    )


class FinishTestResultSchema(Schema):
    id = ID_FIELD
    status = EnumField(ResultStatus, required=True)
    seconds = fields.Float(min=0, required=True)
    message = fields.String(validate=[Length(0)], required=True)
    imageOutput = fields.Integer(required=False, allow_none=True)
    referenceImage = fields.Integer(required=False, allow_none=True)
    diffImage = fields.Integer(required=False, allow_none=True)
    errorValue = fields.Float(required=True, allow_none=True)
    failureReason = EnumField(TestFailureReason, required=False, allow_none=True)


class StartTestResultSchema(Schema):
    id = ID_FIELD
    machineInfo = fields.Nested(MachineInfoSchema, required=True)
