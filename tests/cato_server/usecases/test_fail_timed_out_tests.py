import datetime

from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.fail_timed_out_tests import FailTimedOutTests
from tests.utils import mock_safe


def test_nothing_to_do_should_do_nothing():
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_last_beat_older_than.return_value = []
    test_result_repository = mock_safe(TestResultRepository)
    fail_timed_out_tests = FailTimedOutTests(
        test_result_repository, test_heartbeat_repository
    )

    fail_timed_out_tests.fail_timed_out_tests()

    test_result_repository.save.assert_not_called()


TIMED_OUT_TEST_RESULT = TestResult(
    id=0,
    suite_result_id=1,
    test_name="my_test_name",
    test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
    test_command="my_command",
    test_variables={"testkey": "test_value"},
    machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
    execution_status=ExecutionStatus.NOT_STARTED,
    status=TestStatus.SUCCESS,
    seconds=5,
    message="sucess",
    image_output=2,
    reference_image=3,
    started_at=datetime.datetime.now(),
    finished_at=datetime.datetime.now(),
)

FAILED_TIMED_OUT_TEST_RESULT = TestResult(
    id=0,
    suite_result_id=1,
    test_name="my_test_name",
    test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
    test_command="my_command",
    test_variables={"testkey": "test_value"},
    machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
    execution_status=ExecutionStatus.FINISHED,
    status=TestStatus.FAILED,
    seconds=5,
    message="sucess",
    image_output=2,
    reference_image=3,
    started_at=datetime.datetime.now(),
    finished_at=datetime.datetime.now(),
)


def test_should_fail_test():
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_last_beat_older_than.return_value = [
        TestHeartbeat(id=1, test_result_id=2, last_beat=datetime.datetime.now())
    ]
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = TIMED_OUT_TEST_RESULT
    fail_timed_out_tests = FailTimedOutTests(
        test_result_repository, test_heartbeat_repository
    )

    fail_timed_out_tests.fail_timed_out_tests()

    test_result_repository.save.assert_called_with(FAILED_TIMED_OUT_TEST_RESULT)
