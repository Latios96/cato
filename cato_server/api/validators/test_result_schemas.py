from marshmallow import Schema, fields
from marshmallow.validate import Length
from marshmallow_enum import EnumField

from cato.domain.test_result import TestStatus
from cato.storage.domain.execution_status import ExecutionStatus
from cato_server.api.schemas.general import MachineInfoSchema, ID_FIELD, NAME_FIELD


class CreateTestResultSchema(Schema):
    suite_result_id: ID_FIELD
    test_name: NAME_FIELD
    test_identifier: fields.String(
        required=True, validate=[Length(min=1)]  # todo check is test identifier
    )
    test_command: fields.String(required=True, validate=[Length(1)])
    test_variables: fields.Dict(required=True)
    machine_info: fields.Nested(MachineInfoSchema, required=True)
    execution_status: EnumField(ExecutionStatus, required=True)
    status = EnumField(TestStatus)
    output = fields.List(fields.String())
    seconds = fields.Float(min=1)
    message = fields.String(validate=[Length(1)])
    image_output = fields.Integer()
    reference_image = fields.Integer()
    started_at = fields.DateTime()
    finished_at = fields.DateTime()
