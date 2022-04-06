import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.output import Output
from cato_server.storage.sqlalchemy.sqlalchemy_output_repository import (
    SqlAlchemyOutputRepository,
)


def test_save(sqlalchemy_output_repository, test_result):
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )

    output = sqlalchemy_output_repository.save(output)

    assert output == Output(
        id=1, test_result_id=test_result.id, text="this is a very long text"
    )


def test_save_second_output_for_test_result_should_fail(
    sqlalchemy_output_repository, test_result
):
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    sqlalchemy_output_repository.save(output)

    with pytest.raises(IntegrityError):
        sqlalchemy_output_repository.save(output)


def test_find_by_id_should_find(sqlalchemy_output_repository, test_result):
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    output = sqlalchemy_output_repository.save(output)

    assert sqlalchemy_output_repository.find_by_id(output.id) == output


def test_find_by_id_should_not_find(sqlalchemy_output_repository, test_result):
    assert sqlalchemy_output_repository.find_by_id(1) is None


def test_find_by_test_result_id_should_find(sqlalchemy_output_repository, test_result):
    output = Output(
        id=0, test_result_id=test_result.id, text="this is a very long text"
    )
    output = sqlalchemy_output_repository.save(output)

    assert sqlalchemy_output_repository.find_by_test_result_id(test_result.id) == output


def test_find_by_test_result__id_should_not_find(
    sqlalchemy_output_repository, test_result
):
    assert sqlalchemy_output_repository.find_by_test_result_id(42) is None
