import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.suite_result import SuiteResult
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
    _SuiteResultMapping,
)


def test_to_entity(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )

    entity = sqlalchemy_suite_result_repository.to_entity(suite_result)

    assert entity.id == 1
    assert entity.run_entity_id == run.id
    assert entity.suite_name == "my_suite"
    assert entity.suite_variables == {"key": "value"}


def test_to_domain_object(sqlalchemy_suite_result_repository, run):
    suite_result = sqlalchemy_suite_result_repository.to_domain_object(
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


def test_save(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )

    suite_result = sqlalchemy_suite_result_repository.save(suite_result)

    assert suite_result.id == 1
    assert suite_result.run_id == 1
    assert suite_result.suite_name == "my_suite"
    assert suite_result.suite_variables == {"key": "value"}


def test_save_no_run_id(sqlalchemy_suite_result_repository):
    suite_result = SuiteResult(
        id=1, run_id=0, suite_name="my_suite", suite_variables={"key": "value"}
    )

    with pytest.raises(IntegrityError):
        sqlalchemy_suite_result_repository.save(suite_result)


def test_find_by_id_should_find(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    sqlalchemy_suite_result_repository.save(suite_result)

    assert (
        sqlalchemy_suite_result_repository.find_by_id(suite_result.id).suite_name
        == "my_suite"
    )


def test_find_by_id_should_not_find(sqlalchemy_suite_result_repository):
    assert not sqlalchemy_suite_result_repository.find_by_id(100)


def test_find_by_run_id_should_find(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    saved_suite_result = sqlalchemy_suite_result_repository.save(suite_result)

    assert sqlalchemy_suite_result_repository.find_by_run_id(run.id) == [
        saved_suite_result
    ]


def test_find_by_run_id_should_not_find(sqlalchemy_suite_result_repository):
    assert not sqlalchemy_suite_result_repository.find_by_run_id(100)


def test_find_by_run_id_should_find_in_correct_order(
    sqlalchemy_suite_result_repository, run, order_test_data
):
    names = order_test_data.wrong_order
    suite_results = [
        SuiteResult(id=0, run_id=run.id, suite_name=x, suite_variables={"key": "value"})
        for x in names
    ]

    sqlalchemy_suite_result_repository.insert_many(suite_results)
    result = sqlalchemy_suite_result_repository.find_by_run_id(run.id)
    result_names = list(map(lambda x: x.suite_name.lower(), result))

    assert result_names == order_test_data.correct_order_lowercase


def test_find_by_run_id_with_paging_should_find_in_correct_order(
    sqlalchemy_suite_result_repository, run, order_test_data
):
    names = order_test_data.wrong_order
    suite_results = [
        SuiteResult(id=0, run_id=run.id, suite_name=x, suite_variables={"key": "value"})
        for x in names
    ]

    sqlalchemy_suite_result_repository.insert_many(suite_results)
    result = sqlalchemy_suite_result_repository.find_by_run_id_with_paging(
        run.id, PageRequest(1, 10)
    )
    result_names = list(map(lambda x: x.suite_name.lower(), result.entities))

    assert result_names == order_test_data.correct_order_lowercase


def test_find_by_run_id_with_paging_should_find_empty(
    sqlalchemy_suite_result_repository,
):
    page_request = PageRequest(1, 10)

    assert sqlalchemy_suite_result_repository.find_by_run_id_with_paging(
        100, page_request
    ) == Page.from_page_request(page_request, 0, [])


def test_find_by_run_id_with_paging_should_find_correct(
    sqlalchemy_suite_result_repository, run
):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    saved_suite_result = sqlalchemy_suite_result_repository.save(suite_result)
    page_request = PageRequest(1, 10)

    assert sqlalchemy_suite_result_repository.find_by_run_id_with_paging(
        run.id, page_request
    ) == Page.from_page_request(page_request, 1, [saved_suite_result])


def test_find_by_run_id_and_name_should_find(sqlalchemy_suite_result_repository, run):
    suite_result = SuiteResult(
        id=1, run_id=run.id, suite_name="my_suite", suite_variables={"key": "value"}
    )
    saved_suite_result = sqlalchemy_suite_result_repository.save(suite_result)

    assert (
        sqlalchemy_suite_result_repository.find_by_run_id_and_name(run.id, "my_suite")
        == saved_suite_result
    )


def test_find_by_run_id_and_name_should_not_find(sqlalchemy_suite_result_repository):
    assert not sqlalchemy_suite_result_repository.find_by_run_id_and_name(100, "")


def test_suite_count_by_run_ids_should_be_1(
    sqlalchemy_suite_result_repository, run, suite_result
):
    assert sqlalchemy_suite_result_repository.suite_count_by_run_ids({run.id}) == {
        run.id: 1
    }


def test_suite_count_by_run_ids_should_be_0(sqlalchemy_suite_result_repository, run):
    assert (
        sqlalchemy_suite_result_repository.suite_count_by_run_ids({run.id})[run.id] == 0
    )
