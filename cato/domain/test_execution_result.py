from dataclasses import dataclass
from typing import List

from cato.domain.test import Test
from cato.domain.test_result import TestStatus


@dataclass
class TestExecutionResult:
    test: Test
    result: TestStatus
    output: List[str]
    seconds: float
