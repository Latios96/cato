import pytest

from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.domain.run_status import RunStatus
from cato_server.run_status_calculator import RunStatusCalculator


def make_test_result(unified_test_status: UnifiedTestStatus):
    return TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("suite_name", "test_name"),
        test_command="test_command",
        test_variables={},
        machine_info=MachineInfo("cpu_name", 1, 1),
        unified_test_status=unified_test_status,
    )


def test_calculate_not_started():
    calculator = RunStatusCalculator()

    status = calculator.calculate({UnifiedTestStatus.NOT_STARTED})

    assert status == RunStatus.NOT_STARTED


@pytest.mark.parametrize(
    "test_results",
    [
        {UnifiedTestStatus.RUNNING},
        {
            UnifiedTestStatus.RUNNING,
            UnifiedTestStatus.NOT_STARTED,
        },
    ],
)
def test_calculate_running(test_results):
    calculator = RunStatusCalculator()

    status = calculator.calculate(test_results)

    assert status == RunStatus.RUNNING


def test_calculate_success():
    calculator = RunStatusCalculator()

    status = calculator.calculate({UnifiedTestStatus.SUCCESS})

    assert status == RunStatus.SUCCESS


@pytest.mark.parametrize(
    "test_results",
    [
        {ResultStatus.FAILED},
        {
            ResultStatus.FAILED,
            ResultStatus.SUCCESS,
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
