from dataclasses import dataclass
from enum import Enum


class StatusFilter(Enum):
    NONE = "NONE"  # todo remove None
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


@dataclass
class TestResultFilterOptions:
    status: StatusFilter  # todo instead of None make this optional


# todo implement utils on the typescript site for this
