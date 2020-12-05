from marshmallow import fields, ValidationError
from marshmallow.validate import Regexp, Length, Range

REGEX_VALID_NAME = Regexp(r"^[A-Za-z0-9_\-]+$")


def _is_str_str_dict(the_dict):
    for key, value in the_dict.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValidationError(f"Not a mapping of str->str: {key}={value}")


ID_FIELD = fields.Integer(required=True, validate=[Range(min=0)])
NAME_FIELD = fields.Str(required=True, validate=[Length(min=1), REGEX_VALID_NAME])
VARIABLES_FIELD = fields.Dict(required=True, validate=_is_str_str_dict)
