from dataclasses import dataclass
from typing import List

from cato.domain.test import Test
from cato.domain.test_result import TestResult


@dataclass
class TestExecutionResult:
    test: Test
    result: TestResult
    output: List[str]
    seconds: float