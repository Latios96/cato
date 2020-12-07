from typing import Optional

import pytest

from cato.domain.execution_status import ExecutionStatus
from cato.domain.machine_info import MachineInfo
from cato.domain.run_status import RunStatus
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestResult
from cato.domain.test_status import TestStatus
from cato.reporter.run_status_calculator import RunStatusCalculator


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


def test_calculate_not_started():
    test_results = [make_test_result(ExecutionStatus.NOT_STARTED, None)]
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.NOT_STARTED


@pytest.mark.parametrize(
    "test_results",
    [
        [make_test_result(ExecutionStatus.RUNNING, None)],
        [
            make_test_result(ExecutionStatus.RUNNING, None),
            make_test_result(ExecutionStatus.NOT_STARTED, None),
        ],
        [
            make_test_result(ExecutionStatus.RUNNING, None),
            make_test_result(ExecutionStatus.NOT_STARTED, None),
            make_test_result(ExecutionStatus.FINISHED, None),
        ],
        [
            make_test_result(ExecutionStatus.NOT_STARTED, None),
            make_test_result(ExecutionStatus.FINISHED, None),
        ],
    ],
)
def test_calculate_running(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.RUNNING


@pytest.mark.parametrize(
    "test_results",
    [
        [make_test_result(ExecutionStatus.FINISHED, TestStatus.SUCCESS)],
        [
            make_test_result(ExecutionStatus.FINISHED, TestStatus.SUCCESS),
            make_test_result(ExecutionStatus.FINISHED, TestStatus.SUCCESS),
        ],
    ],
)
def test_calculate_success(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.SUCCESS


@pytest.mark.parametrize(
    "test_results",
    [
        [make_test_result(ExecutionStatus.FINISHED, TestStatus.FAILED)],
        [
            make_test_result(ExecutionStatus.FINISHED, TestStatus.FAILED),
            make_test_result(ExecutionStatus.FINISHED, TestStatus.SUCCESS),
        ],
    ],
)
def test_calculate_failed(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.FAILED
