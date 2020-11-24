from typing import Dict

import attr


@attr.s
class Test:
    name: str = attr.ib()
    command: str = attr.ib()
    variables: Dict[str, str] = attr.ib()

    def to_dict(self):
        return {"name": self.name, "command": self.command}

    @name.validator
    def check(self, attribute, value):
        if not value:
            raise ValueError("Test name can not be empty!")

        for c in value:
            if c in [' ', '/',",", ".", "\\", "\"", "'"]:
                raise ValueError(f"Test name {value} contains not allowed character: {c}")