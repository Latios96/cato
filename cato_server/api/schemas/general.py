from marshmallow.validate import Regexp

REGEX_VALID_NAME = Regexp(r"^[A-Za-z0-9_\-]+$")
