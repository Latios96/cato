from typing import Optional

import pytest

from cato_server.domain.execution_status import ExecutionStatus
from cato_common.domain.machine_info import MachineInfo
from cato_server.domain.run_status import RunStatus
from cato_common.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato.domain.test_status import TestStatus
from cato_server.run_status_calculator import RunStatusCalculator


def make_test_result(
    execution_status: ExecutionStatus, test_status: Optional[TestStatus]
):
    return TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("suite_name", "test_name"),
        test_command="test_command",
        test_variables={},
        machine_info=MachineInfo("cpu_name", 1, 1),
        execution_status=execution_status,
        status=test_status,
    )


@pytest.mark.parametrize(
    "status_set",
    [
        {(ExecutionStatus.NOT_STARTED, None)},
        {
            (ExecutionStatus.NOT_STARTED, None),
            (ExecutionStatus.FINISHED, TestStatus.FAILED),
        },
        {
            (ExecutionStatus.NOT_STARTED, None),
            (ExecutionStatus.FINISHED, TestStatus.SUCCESS),
        },
    ],
)
def test_calculate_not_started(status_set):
    calculator = RunStatusCalculator()

    status = calculator.calculate(status_set)

    assert status == RunStatus.NOT_STARTED


@pytest.mark.parametrize(
    "test_results",
    [
        {(ExecutionStatus.RUNNING, None)},
        {
            (ExecutionStatus.RUNNING, None),
            (ExecutionStatus.NOT_STARTED, None),
        },
        {
            (ExecutionStatus.RUNNING, None),
            (ExecutionStatus.NOT_STARTED, None),
            (ExecutionStatus.FINISHED, None),
        },
    ],
)
def test_calculate_running(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.RUNNING


@pytest.mark.parametrize(
    "test_results",
    [
        {(ExecutionStatus.FINISHED, TestStatus.SUCCESS)},
        {
            (ExecutionStatus.FINISHED, TestStatus.SUCCESS),
            (ExecutionStatus.FINISHED, TestStatus.SUCCESS),
        },
    ],
)
def test_calculate_success(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.SUCCESS


@pytest.mark.parametrize(
    "test_results",
    [
        {(ExecutionStatus.FINISHED, TestStatus.FAILED)},
        {
            (ExecutionStatus.FINISHED, TestStatus.FAILED),
            (ExecutionStatus.FINISHED, TestStatus.SUCCESS),
        },
    ],
)
def test_calculate_failed(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.FAILED


def test_empty_run():
    calculator = RunStatusCalculator()

    status = calculator.calculate(set())

    assert status == RunStatus.NOT_STARTED
