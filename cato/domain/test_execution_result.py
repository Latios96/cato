import datetime
from dataclasses import dataclass
from typing import List, Optional

from cato.domain.test import Test
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.test_failure_reason import TestFailureReason


@dataclass
class TestExecutionResult:
    test: Test
    status: ResultStatus
    output: List[str]
    seconds: float
    message: str
    image_output: Optional[int]
    reference_image: Optional[int]
    diff_image: Optional[int]
    started_at: datetime.datetime
    finished_at: datetime.datetime
    error_value: Optional[float]
    failure_reason: Optional[TestFailureReason]

    __test__ = False
