from dataclasses import dataclass
from typing import Optional


@dataclass
class File:
    id: int
    name: str
    hash: str
    value_counter: int
    byte_count: Optional[int]
