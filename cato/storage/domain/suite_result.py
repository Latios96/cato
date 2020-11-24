from dataclasses import dataclass
from typing import Dict

from cato.domain.test_suite_execution_result import TestSuiteExecutionResult


@dataclass
class SuiteResult:
    id: int
    run_id: int
    suite_name: str
    suite_variables: Dict[str, str]

    @staticmethod
    def from_test_suite_execution_result(result: TestSuiteExecutionResult):
        return SuiteResult(
            id=0,
            run_id=0,
            suite_name=result.test_suite.name,
            suite_variables=result.test_suite.variables,
        )
