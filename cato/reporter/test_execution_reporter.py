from typing import List

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
)
from cato_server.domain.test_identifier import TestIdentifier


class TestExecutionReporter:
    def start_execution(self, project_name: str, test_suites: List[TestSuite]):
        raise NotImplementedError()

    def report_test_execution_start(self, current_suite: TestSuite, test: Test):
        raise NotImplementedError()

    def report_test_result(
        self, current_suite: TestSuite, test_execution_result: TestExecutionResult
    ):
        raise NotImplementedError()

    def report_heartbeat(self, test_identifier: TestIdentifier):
        raise NotImplementedError()

    def report_test_execution_end(
        self, last_run_information_repository: LastRunInformationRepository
    ):
        raise NotImplementedError()
