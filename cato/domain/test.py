from typing import Dict

import attr

from cato.domain.validation import validate_name


@attr.s
class Test:
    name: str = attr.ib()
    command: str = attr.ib()
    variables: Dict[str, str] = attr.ib()

    def to_dict(self):
        return {"name": self.name, "command": self.command}

    @name.validator
    def check(self, attribute, value):
        validate_name(value)

    __test__ = False
