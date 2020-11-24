import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.domain.test_result import TestResult
from cato.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_save_success(sessionmaker_fixture, suite_result):
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
        execution_status="NOT_STARTED",
        status=TestStatus.SUCCESS,
        output=["1", "2", "3"],
        seconds=5,
        message="sucess",
        image_output="image_output",
        reference_image="reference_image",
        started_at=start_time,
        finished_at=end_time,
    )

    test_result_save = repository.save(test_result)

    test_result.id = test_result_save.id

    assert test_result_save == test_result


def test_save_no_suite_result(sessionmaker_fixture):
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
        execution_status="NOT_STARTED",
        status=TestStatus.SUCCESS,
        output=["1", "2", "3"],
        seconds=5,
        message="sucess",
        image_output="image_output",
        reference_image="reference_image",
        started_at=start_time,
        finished_at=end_time,
    )
    with pytest.raises(IntegrityError):
        test_result_save = repository.save(test_result)


def test_find_by_suite_result_and_test_identifier(sessionmaker_fixture, suite_result):
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
        execution_status="NOT_STARTED",
        status=TestStatus.SUCCESS,
        output=["1", "2", "3"],
        seconds=5,
        message="sucess",
        image_output="image_output",
        reference_image="reference_image",
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
