from marshmallow import Schema, fields, EXCLUDE

from cato_server.api.schemas.general import ID_FIELD


class CreateRunSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    project_id = ID_FIELD
    started_at = fields.DateTime()
