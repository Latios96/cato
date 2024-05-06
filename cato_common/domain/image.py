from dataclasses import dataclass
from enum import Enum
from typing import List


class ImageTranscodingState(str, Enum):
    WAITING_FOR_TRANSCODING = "WAITING_FOR_TRANSCODING"
    TRANSCODED = "TRANSCODED"


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
    width: int
    height: int
    transcoding_state: ImageTranscodingState
