from marshmallow import Schema, fields

from cato_server.api.schemas.general import ID_FIELD
from cato_server.api.schemas.run_schemas import ComparisonSettingsSchema


class CreateComparisonSettingsEditSchema(Schema):
    testResultId = ID_FIELD
    newValue = fields.Nested(ComparisonSettingsSchema, required=True)


class CreateReferenceImageSettingsEditSchema(Schema):
    testResultId = ID_FIELD
