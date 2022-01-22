from dataclasses import dataclass


@dataclass
class TestResultStatusInformation:
    __test__ = False

    not_started: int
    running: int
    failed: int
    success: int
