from email_validator import validate_email


class Email:
    def __init__(self, value):
        value = value.strip()
        if not value:
            raise ValueError("A email address can not be empty or blank.")
        self._value = validate_email(value.lower(), check_deliverability=False).email

    def __repr__(self):
        return self._value

    def __str__(self):
        return self._value

    def __eq__(self, other):
        return self._value == other._value

    def __hash__(self):
        return hash(self._value)
