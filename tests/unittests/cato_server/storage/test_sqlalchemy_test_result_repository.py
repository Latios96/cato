import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.test_identifier import TestIdentifier
from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.test_result import TestResult
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_save_success(sessionmaker_fixture, suite_result, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )

    test_result_save = repository.save(test_result)

    test_result.id = test_result_save.id

    assert test_result_save == test_result


def test_save_no_suite_result(sessionmaker_fixture, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=0,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    with pytest.raises(IntegrityError):
        repository.save(test_result)


def test_find_by_suite_result_and_test_identifier(
    sessionmaker_fixture, suite_result, stored_image
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    test_result_save = repository.save(test_result)

    result = repository.find_by_suite_result_and_test_identifier(
        suite_result.id, TestIdentifier("my_suite", "my_test")
    )

    assert result.id == test_result_save.id


def test_find_find_by_suite_result_and_test_identifier_not_found(sessionmaker_fixture):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert not repository.find_by_suite_result_and_test_identifier(
        3, TestIdentifier("my_suite", "my_test")
    )


def test_find_by_suite_result(sessionmaker_fixture, suite_result, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        execution_status=ExecutionStatus.NOT_STARTED,
        status=TestStatus.SUCCESS,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    test_result_save = repository.save(test_result)

    results = repository.find_by_suite_result_id(suite_result.id)

    assert results == [test_result_save]


def test_find_by_suite_result_not_found(sessionmaker_fixture, suite_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_suite_result_id(suite_result.id)

    assert results == []


def test_find_by_run_id_should_find_single_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_suite_result_id(run.id)

    assert results == [test_result]


def test_find_by_run_id_should_find_multiple(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result1 = repository.save(test_result)
    test_result.id = 0
    test_result2 = repository.save(test_result)
    test_result.id = 0
    test_result3 = repository.save(test_result)
    test_result.id = 1

    results = repository.find_by_suite_result_id(run.id)

    assert results == [test_result, test_result1, test_result2, test_result3]


def test_find_by_run_id_should_find_empty_list(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_suite_result_id(run.id)

    assert results == []


def test_find_execution_status_by_run_ids_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result1 = repository.save(test_result)
    test_result.id = 0
    test_result2 = repository.save(test_result)
    test_result.id = 0
    test_result3 = repository.save(test_result)
    test_result.id = 1

    results = repository.find_execution_status_by_run_ids({run.id})

    assert results == {
        run.id: {
            (ExecutionStatus.NOT_STARTED, TestStatus.SUCCESS),
            (ExecutionStatus.NOT_STARTED, TestStatus.SUCCESS),
            (ExecutionStatus.NOT_STARTED, TestStatus.SUCCESS),
        }
    }


def test_find_execution_status_by_run_ids_should_find_empty_list(
    sessionmaker_fixture, run
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_execution_status_by_run_ids({run.id})

    assert results == {}


def test_find_execution_status_by_project_id_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_project_id(run.project_id)

    assert result == {run.id: {(ExecutionStatus.NOT_STARTED, TestStatus.SUCCESS)}}


def test_find_execution_status_by_project_id_should_not_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_project_id(42)

    assert result == {}


def test_test_count_by_run_id_should_find_one(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.test_count_by_run_id(run.id) == 1


def test_test_count_by_run_id_should_find_nothing(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.test_count_by_run_id(run.id) == 0


def test_failed_test_count_by_run_id_should_find_nothing(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.failed_test_count_by_run_id(run.id) == 0


def test_failed_test_count_by_run_id_should_find_nothing_because_only_success(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.failed_test_count_by_run_id(run.id) == 0


def test_failed_test_count_by_run_id_should_find_one(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.status = TestStatus.FAILED
    repository.save(test_result)

    assert repository.failed_test_count_by_run_id(run.id) == 1


def test_duration_by_run_id_single_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_id(run.id) == test_result.seconds


def test_duration_by_run_id_multiple_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    repository.save(test_result)

    assert repository.duration_by_run_id(run.id) == 10


def test_duration_by_run_id_no_tests(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_id(run.id) == 0


def test_find_execution_status_by_suite_ids(
    sessionmaker_fixture, suite_result, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_suite_ids({suite_result.id})

    assert result == {
        suite_result.id: {(ExecutionStatus.NOT_STARTED, TestStatus.SUCCESS)}
    }


def test_find_execution_status_by_suite_ids_should_return_empty(
    sessionmaker_fixture, suite_result, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_suite_ids({42})

    assert result == {}


def test_find_by_run_id_and_test_identifier_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_and_test_identifier(
        run.id, test_result.test_identifier
    )

    assert result == test_result


def test_find_by_run_id_and_test_identifier_should_not_find(
    sessionmaker_fixture, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_and_test_identifier(
        42, test_result.test_identifier
    )

    assert result is None


def test_find_by_run_id_filter_by_test_status_should_not_find_not_existing_run_id(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(42, TestStatus.SUCCESS)

    assert result == []


def test_find_by_run_id_filter_by_test_status_should_not_find_not_matching_status(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(run.id, TestStatus.FAILED)

    assert result == []


def test_find_by_run_id_filter_by_test_status_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(run.id, TestStatus.SUCCESS)

    assert result == [test_result]