import datetime
from dataclasses import dataclass
from typing import List, Optional

from cato.domain.test import Test
from cato.domain.test_status import TestStatus


@dataclass
class TestExecutionResult:
    test: Test
    status: TestStatus
    output: List[str]
    seconds: float
    message: str
    image_output: Optional[int]
    reference_image: Optional[int]
    diff_image: Optional[int]
    started_at: datetime.datetime
    finished_at: datetime.datetime

    __test__ = False
