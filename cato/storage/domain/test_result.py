import datetime
from dataclasses import dataclass
from typing import Dict, List

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus


@dataclass
class TestResult:
    id: int
    suite_result_id: int
    test_name: str
    test_identifier: TestIdentifier
    test_command: str
    test_variables: Dict[str, str]
    execution_status: str
    status: TestStatus
    output: List[str]
    seconds: float
    message: str
    image_output: str
    reference_image: str
    started_at: datetime.datetime
    finished_at: datetime.datetime
