import datetime

from cato.domain.machine_info import MachineInfo
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.mappers.test_result_class_mapper import TestResultClassMapper
from cato.storage.domain.execution_status import ExecutionStatus
from cato.storage.domain.test_result import TestResult


def test_map_from_with_required_only():
    mapper = TestResultClassMapper()
    data = {
        "execution_status": "NOT_STARTED",
        "id": 0,
        "suite_result_id": 1,
        "test_name": "test_name",
        "test_identifier": "my_suite/test_name",
        "test_command": "my_command",
        "test_variables": {"key": "value"},
        "machine_info": {"cores": 8, "cpu_name": "Intel Xeon", "memory": 2},
    }

    result = mapper.map_from_dict(data)

    assert result == TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("my_suite", "test_name"),
        test_command="my_command",
        test_variables={"key": "value"},
        machine_info=MachineInfo("Intel Xeon", 8, 2),
        execution_status=ExecutionStatus.NOT_STARTED,
    )


def test_map_from_with_optional():
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    mapper = TestResultClassMapper()
    data = {
        "id": 0,
        "suite_result_id": 1,
        "test_name": "test_name",
        "test_identifier": "my_suite/test_name",
        "test_command": "my_command",
        "test_variables": {"key": "value"},
        "machine_info": {"cores": 8, "cpu_name": "Intel Xeon", "memory": 2},
        "execution_status": "NOT_STARTED",
        "status": "SUCCESS",
        "output": ["1", "2", "3"],
        "seconds": 1,
        "message": "message",
        "image_output": 1,
        "reference_image": 2,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
    }

    result = mapper.map_from_dict(data)

    assert result == TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("my_suite", "test_name"),
        test_command="my_command",
        test_variables={"key": "value"},
        machine_info=MachineInfo("Intel Xeon", 8, 2),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        output=["1", "2", "3"],
        seconds=1,
        message="message",
        image_output=1,
        reference_image=2,
        started_at=started_at,
        finished_at=finished_at,
    )


def test_map_to_with_required_only():
    mapper = TestResultClassMapper()
    test_result = TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("my_suite", "test_name"),
        test_command="my_command",
        test_variables={"key": "value"},
        machine_info=MachineInfo("Intel Xeon", 8, 2),
        execution_status=ExecutionStatus.NOT_STARTED,
    )

    result = mapper.map_to_dict(test_result)

    assert result == {
        "execution_status": "NOT_STARTED",
        "id": 0,
        "suite_result_id": 1,
        "test_name": "test_name",
        "test_identifier": "my_suite/test_name",
        "test_command": "my_command",
        "test_variables": {"key": "value"},
        "machine_info": {"cores": 8, "cpu_name": "Intel Xeon", "memory": 2},
    }


def test_map_to_with_optional():
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    mapper = TestResultClassMapper()
    test_result = TestResult(
        id=0,
        suite_result_id=1,
        test_name="test_name",
        test_identifier=TestIdentifier("my_suite", "test_name"),
        test_command="my_command",
        test_variables={"key": "value"},
        machine_info=MachineInfo("Intel Xeon", 8, 2),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        output=["1", "2", "3"],
        seconds=1,
        message="message",
        image_output=1,
        reference_image=2,
        started_at=started_at,
        finished_at=finished_at,
    )

    result = mapper.map_to_dict(test_result)

    assert result == {
        "id": 0,
        "suite_result_id": 1,
        "test_name": "test_name",
        "test_identifier": "my_suite/test_name",
        "test_command": "my_command",
        "test_variables": {"key": "value"},
        "machine_info": {"cores": 8, "cpu_name": "Intel Xeon", "memory": 2},
        "execution_status": "NOT_STARTED",
        "status": "SUCCESS",
        "output": ["1", "2", "3"],
        "seconds": 1,
        "message": "message",
        "image_output": 1,
        "reference_image": 2,
        "started_at": started_at.isoformat(),
        "finished_at": finished_at.isoformat(),
    }
