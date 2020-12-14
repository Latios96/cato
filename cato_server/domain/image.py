from dataclasses import dataclass
from typing import List


@dataclass
class ImageChannel:
    id: int
    image_id: int
    name: str
    file_id: int


@dataclass
class Image:
    id: int
    name: str
    original_file_id: int
    channels: List[ImageChannel]
