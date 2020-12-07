import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.output import Output
from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)


def test_save(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )

    output = repository.save(output)

    assert output == Output(
        id=1, test_result_id=test_result.id, text="this is a very long text"
    )


def test_save_second_output_for_test_result_should_fail(
    sessionmaker_fixture, test_result
):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    repository.save(output)

    with pytest.raises(IntegrityError):
        repository.save(output)


def test_find_by_id_should_find(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    output = repository.save(output)

    assert repository.find_by_id(output.id) == output


def test_find_by_id_should_not_find(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)

    assert repository.find_by_id(1) is None


def test_find_by_test_result_id_should_find(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    output = repository.save(output)

    assert repository.find_by_test_result_id(test_result.id) == output


def test_find_by_test_result__id_should_not_find(sessionmaker_fixture, test_result):
    repository = SqlAlchemyOutputRepository(sessionmaker_fixture)

    assert repository.find_by_test_result_id(42) is None
