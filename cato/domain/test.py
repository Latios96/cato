from dataclasses import dataclass
from typing import List


@dataclass
class Test:
    name: str
    command: List[str]
