from marshmallow import Schema, fields

from cato_server.api.schemas.general import ID_FIELD
from cato_server.api.schemas.run_schemas import ComparisonSettingsSchema


class CreateComparisonSettingsEditSchema(Schema):
    test_result_id = ID_FIELD
    new_value = fields.Nested(ComparisonSettingsSchema, required=True)


class CreateReferenceImageSettingsEditSchema(Schema):
    test_result_id = ID_FIELD
