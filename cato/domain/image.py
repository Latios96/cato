from dataclasses import dataclass
from typing import List


@dataclass
class Channel:
    name: str
    file: int


@dataclass
class Image:
    id: int
    name: str
    original_file: int
    channels: List[Channel]
