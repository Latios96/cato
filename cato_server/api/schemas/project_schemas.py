from marshmallow import Schema, fields, EXCLUDE
from marshmallow.validate import Length

from cato_server.api.schemas.general import REGEX_VALID_NAME


class CreateProjectSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.Str(required=True, validate=[Length(min=1), REGEX_VALID_NAME])
