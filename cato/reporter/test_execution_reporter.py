from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_suite import TestSuite
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato_common.domain.test_identifier import TestIdentifier


class TestExecutionReporter:
    def start_execution(self, config: RunConfig) -> None:
        raise NotImplementedError()

    def use_run_id(self, run_id: int) -> None:
        raise NotImplementedError()

    def run_id(self) -> int:
        raise NotImplementedError()

    def report_test_execution_start(self, current_suite: TestSuite, test: Test) -> None:
        raise NotImplementedError()

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ) -> None:
        raise NotImplementedError()

    def report_heartbeat(self, test_identifier: TestIdentifier) -> None:
        raise NotImplementedError()

    def report_test_execution_end(
        self, last_run_information_repository: LastRunInformationRepository
    ) -> None:
        raise NotImplementedError()

    def report_performance_trace(self, performance_trace_json: str) -> None:
        raise NotImplementedError()
