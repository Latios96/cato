from enum import Enum


class TestStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

    __test__ = False
