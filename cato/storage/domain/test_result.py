import datetime
from dataclasses import dataclass
from typing import Dict, List

import attr

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.domain.execution_status import ExecutionStatus


@attr.s
class TestResult:
    id: int = attr.ib()
    suite_result_id: int = attr.ib()
    test_name: str = attr.ib()
    test_identifier: TestIdentifier = attr.ib()
    test_command: str = attr.ib()
    test_variables: Dict[str, str] = attr.ib()
    execution_status: ExecutionStatus = attr.ib(default=ExecutionStatus.NOT_STARTED)
    status: TestStatus = attr.ib(default=None)
    output: List[str] = attr.ib(factory=list)
    seconds: float = attr.ib(default=0)
    message: str = attr.ib(default="")
    image_output: int = attr.ib(default="")
    reference_image: int = attr.ib(default="")
    started_at: datetime.datetime = attr.ib(default=None)
    finished_at: datetime.datetime = attr.ib(default=None)
