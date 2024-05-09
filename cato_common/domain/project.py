from dataclasses import dataclass
from enum import Enum


class ProjectStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ARCHIVED = "ARCHIVED"


@dataclass
class Project:
    id: int
    name: str
    status: ProjectStatus
