from dataclasses import dataclass
from enum import Enum


class StatusFilter(Enum):
    NONE = "NONE"
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


@dataclass
class TestResultFilterOptions:
    status: StatusFilter
