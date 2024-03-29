import pathvalidate
from marshmallow import fields, ValidationError, Schema, EXCLUDE
from marshmallow.validate import Regexp, Length, Range
from pathvalidate import validate_filename, validate_filepath

REGEX_VALID_NAME = Regexp(r"^[A-Za-z0-9_ \-]+$")


def _is_str_str_dict(the_dict):
    for key, value in the_dict.items():
        if not isinstance(key, str) or not isinstance(value, str):
            raise ValidationError(f"Not a mapping of str->str: {key}={value}")


def _validate_filename(name):
    try:
        validate_filename(name)
    except pathvalidate.ValidationError as e:
        raise ValidationError(str(e))


def _validate_filepath(name):
    error = None
    for platform in ["Linux", "macOS", "Windows"]:
        try:
            validate_filepath(name, platform=platform)
            return True
        except pathvalidate.ValidationError as e:
            error = e
    raise ValidationError(str(error))


ID_FIELD = fields.Integer(required=True, validate=[Range(min=0)])
NAME_FIELD = fields.Str(required=True, validate=[Length(min=1), _validate_filename])
FILE_PATH_FIELD = fields.Str(
    required=True, validate=[Length(min=1), _validate_filepath]
)
VARIABLES_FIELD = fields.Dict(required=True, validate=_is_str_str_dict)
OPTIONAL_VARIABLES_FIELD = fields.Dict(validate=_is_str_str_dict)


class MachineInfoSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    cpuName = fields.String(required=True, validate=[Length(min=1)])
    cores = fields.Integer(required=True, validate=[Range(min=1)])
    memory = fields.Float(required=True, validate=[Range(min=0)])
