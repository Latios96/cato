from marshmallow import Schema, EXCLUDE

from cato_server.api.schemas.general import ID_FIELD, NAME_FIELD, VARIABLES_FIELD


class CreateSuiteResultSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    run_id = ID_FIELD
    suite_name = NAME_FIELD
    suite_variables = VARIABLES_FIELD
