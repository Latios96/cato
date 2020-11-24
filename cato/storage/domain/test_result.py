import datetime
from dataclasses import dataclass
from typing import Dict, List

import attr

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus


@attr.s
class TestResult:
    id: int = attr.ib()
    suite_result_id: int = attr.ib()
    test_name: str = attr.ib()
    test_identifier: TestIdentifier = attr.ib()
    test_command: str = attr.ib()
    test_variables: Dict[str, str] = attr.ib()
    execution_status: str = attr.ib(default="NOT_STARTED")  # todo use enum
    status: TestStatus = attr.ib(default=None)
    output: List[str] = attr.ib(factory=list)
    seconds: float = attr.ib(default=0)
    message: str = attr.ib(default="")
    image_output: str = attr.ib(default="")
    reference_image: str = attr.ib(default="")
    started_at: datetime.datetime = attr.ib(default=None)
    finished_at: datetime.datetime = attr.ib(default=None)
