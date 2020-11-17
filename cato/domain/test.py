from dataclasses import dataclass
from typing import Dict


@dataclass
class Test:
    name: str
    command: str
    variables: Dict[str, str]

    def to_dict(self):
        return {
            'name': self.name,
            'command': self.command
        }