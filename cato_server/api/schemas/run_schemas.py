from marshmallow import Schema, fields

from cato_server.api.schemas.general import ID_FIELD


class CreateRunSchema(Schema):
    project_id = ID_FIELD
    started_at = fields.DateTime()
