from marshmallow import Schema, fields
from marshmallow.validate import Length

from cato_server.api.schemas.general import REGEX_VALID_NAME


class CreateProjectSchema(Schema):
    name = fields.Str(required=True, validate=[Length(min=1), REGEX_VALID_NAME])
