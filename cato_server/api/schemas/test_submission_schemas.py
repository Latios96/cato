# submission info
# config
# test suite
# tests
from marshmallow import Schema, EXCLUDE

from cato_server.api.schemas.general import ID_FIELD, FILE_PATH_FIELD


class SubmissionInfoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    run_id = ID_FIELD
    resource_path = FILE_PATH_FIELD
    executable = FILE_PATH_FIELD
