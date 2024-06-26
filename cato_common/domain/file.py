from dataclasses import dataclass


@dataclass
class File:
    id: int
    name: str
    hash: str
    value_counter: int
