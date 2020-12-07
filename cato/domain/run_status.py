from enum import Enum


class RunStatus(str, Enum):
    NOT_STARTED = "NOT_STARTED"
    RUNNING = "RUNNING"
    FINISHED = "FINISHED"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
