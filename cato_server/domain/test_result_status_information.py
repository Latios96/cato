from dataclasses import dataclass


@dataclass
class TestResultStatusInformation:
    not_started: int
    running: int
    failed: int
    success: int
