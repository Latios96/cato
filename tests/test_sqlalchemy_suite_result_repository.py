import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.run import Run
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.sqlalchemy.sqlalchemy_run_repository import SqlAlchemyRunRepository
from cato.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
    _SuiteResultMapping,
)


def test_to_entity(sessionmaker_fixture, run):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )

    entity = repository.to_entity(suite_result)

    assert entity.id == 1
    assert entity.run_entity_id == run.id
    assert entity.suite_name == "my_suite"
    assert entity.suite_variables == {"key": "value"}


def test_to_domain_object(sessionmaker_fixture, run):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)

    suite_result = repository.to_domain_object(
        _SuiteResultMapping(
            id=1,
            run_entity_id=run.id,
            suite_name="my_suite",
            suite_variables={"key": "value"},
        )
    )

    assert suite_result.id == 1
    assert suite_result.run_id == run.id
    assert suite_result.suite_name == "my_suite"
    assert suite_result.suite_variables == {"key": "value"}


def test_save(sessionmaker_fixture, run):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )

    suite_result = repository.save(suite_result)

    assert suite_result.id == 1
    assert suite_result.run_id == 1
    assert suite_result.suite_name == "my_suite"
    assert suite_result.suite_variables == {"key": "value"}


def test_save_no_run_id(sessionmaker_fixture):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    suite_result = SuiteResult(
        id=1, run_id=0, suite_name="my_suite", suite_variables={"key": "value"}
    )

    with pytest.raises(IntegrityError):
        run = repository.save(suite_result)


def test_find_by_id_should_find(sessionmaker_fixture, run):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    repository.save(suite_result)

    assert repository.find_by_id(suite_result.id).suite_name == "my_suite"


def test_find_by_id_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)

    assert not repository.find_by_id(100)
