from dataclasses import dataclass
from typing import List


@dataclass
class ImageChannel:
    name: str
    file_id: int


@dataclass
class Image:
    id: int
    name: str
    original_file_id: int
    channels: List[ImageChannel]
