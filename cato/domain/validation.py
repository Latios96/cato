from pathvalidate import validate_filename, ValidationError


def validate_name(name):
    if not name:
        raise ValueError("Test name can not be empty!")

    validate_filename(name)
