from dataclasses import dataclass
from enum import Enum
from typing import Optional


class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


@dataclass
class Project:
    id: int
    name: str
    status: ProjectStatus
    thumbnail_file_id: Optional[int] = None
