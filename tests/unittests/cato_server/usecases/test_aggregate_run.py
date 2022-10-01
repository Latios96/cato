import datetime

import pytest

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.run_aggregate import RunAggregate, RunProgress
from cato_server.domain.run_status import RunStatus
from cato_server.domain.test_result_status_information import (
    TestResultStatusInformation,
)
from cato_server.run_status_calculator import RunStatusCalculator
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.aggregate_run import AggregateRun
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.mock_test_result_repository = mock_safe(TestResultRepository)
            self.mock_suite_result_repository = mock_safe(SuiteResultRepository)
            self.mock_run_status_calculator = mock_safe(RunStatusCalculator)
            self.aggregate_run = AggregateRun(
                self.mock_test_result_repository,
                self.mock_suite_result_repository,
                self.mock_run_status_calculator,
            )

    return TestContext()


def test_aggregate_empty_page(test_context):
    aggregated_page = test_context.aggregate_run.aggregate_runs_by_project_id(1, [])

    assert aggregated_page == []


def test_aggregate_page(test_context, local_computer_run_information):
    test_context.mock_test_result_repository.find_status_by_project_id.return_value = {
        1: {UnifiedTestStatus.SUCCESS},
        2: {UnifiedTestStatus.FAILED},
    }
    test_context.mock_test_result_repository.duration_by_run_ids.return_value = {
        1: 1,
        2: 2,
    }
    test_context.mock_test_result_repository.test_count_by_run_ids.return_value = {
        1: 10,
        2: 10,
    }
    test_context.mock_test_result_repository.status_information_by_run_ids.return_value = {
        1: TestResultStatusInformation(not_started=1, running=2, failed=3, success=4),
        2: TestResultStatusInformation(not_started=1, running=2, failed=3, success=4),
    }

    test_context.mock_run_status_calculator.calculate.side_effect = (
        lambda x: RunStatus.SUCCESS if x == 1 else RunStatus.FAILED
    )
    test_context.mock_suite_result_repository.suite_count_by_run_ids.return_value = {
        1: 1,
        2: 2,
    }
    runs = [
        Run(
            id=1,
            project_id=1,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            branch_name=BranchName("main"),
            previous_run_id=None,
            run_information=local_computer_run_information,
        ),
        Run(
            id=2,
            project_id=1,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            branch_name=BranchName("main"),
            previous_run_id=None,
            run_information=local_computer_run_information,
        ),
    ]

    aggregated_runs = test_context.aggregate_run.aggregate_runs_by_project_id(1, runs)

    assert aggregated_runs == [
        RunAggregate(
            id=1,
            project_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            status=RunStatus.FAILED,
            duration=1,
            branch_name=BranchName(name="main"),
            run_information=local_computer_run_information,
            suite_count=1,
            test_count=10,
            progress=RunProgress(
                waiting_test_count=1,
                running_test_count=2,
                failed_test_count=3,
                succeeded_test_count=4,
                progress_percentage=0.9,
            ),
        ),
        RunAggregate(
            id=2,
            project_id=2,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            status=RunStatus.FAILED,
            duration=2,
            branch_name=BranchName(name="main"),
            run_information=local_computer_run_information,
            suite_count=2,
            test_count=10,
            progress=RunProgress(
                waiting_test_count=1,
                running_test_count=2,
                failed_test_count=3,
                succeeded_test_count=4,
                progress_percentage=0.9,
            ),
        ),
    ]
    test_context.mock_test_result_repository.find_status_by_project_id.assert_called_with(
        1
    )
    test_context.mock_test_result_repository.duration_by_run_ids.assert_called_with(
        {1, 2}
    )
    test_context.mock_run_status_calculator.calculate.assert_any_call(
        {UnifiedTestStatus.FAILED}
    )
    test_context.mock_run_status_calculator.calculate.assert_any_call(
        {UnifiedTestStatus.SUCCESS}
    )
    test_context.mock_test_result_repository.test_count_by_run_ids.assert_called_with(
        {1, 2}
    )
    test_context.mock_test_result_repository.status_information_by_run_ids.assert_called_with(
        {1, 2}
    )
    test_context.mock_suite_result_repository.suite_count_by_run_ids.assert_called_with(
        {1, 2}
    )


def test_aggregate_run_without_suites_and_tests(
    test_context, local_computer_run_information
):
    test_context.mock_test_result_repository.find_status_by_project_id.return_value = {
        1: {UnifiedTestStatus.SUCCESS},
    }
    test_context.mock_test_result_repository.duration_by_run_ids.return_value = {
        1: 0,
    }
    test_context.mock_test_result_repository.test_count_by_run_ids.return_value = {
        1: 0,
    }
    test_context.mock_test_result_repository.status_information_by_run_ids.return_value = {
        1: TestResultStatusInformation(not_started=0, running=0, failed=0, success=0),
    }

    test_context.mock_run_status_calculator.calculate.side_effect = (
        lambda x: RunStatus.SUCCESS if x == 1 else RunStatus.FAILED
    )
    test_context.mock_suite_result_repository.suite_count_by_run_ids.return_value = {
        1: 1,
        2: 2,
    }
    runs = [
        Run(
            id=1,
            project_id=1,
            run_batch_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            branch_name=BranchName("main"),
            previous_run_id=None,
            run_information=local_computer_run_information,
        ),
    ]

    aggregated_runs = test_context.aggregate_run.aggregate_runs_by_project_id(1, runs)

    assert aggregated_runs == [
        RunAggregate(
            id=1,
            project_id=1,
            started_at=datetime.datetime(year=2022, month=9, day=30),
            status=RunStatus.FAILED,
            duration=0,
            branch_name=BranchName(name="main"),
            run_information=local_computer_run_information,
            suite_count=1,
            test_count=0,
            progress=RunProgress(
                waiting_test_count=0,
                running_test_count=0,
                failed_test_count=0,
                succeeded_test_count=0,
                progress_percentage=0,
            ),
        )
    ]
