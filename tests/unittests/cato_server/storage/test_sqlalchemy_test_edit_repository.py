import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.test_edit import TestEdit, EditTypes
from cato_server.storage.sqlalchemy.sqlalchemy_test_edit_repository import (
    SqlAlchemyTestEditRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_save(test_result, sessionmaker_fixture):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = TestEdit(
        id=0,
        test_id=test_result.id,
        edit_type=EditTypes.COMPARISON_SETTINGS,
        created_at=datetime.datetime.now(),
        old_value={"key": "value"},
        new_value={"key": "new value"},
    )

    saved_test_edit = repository.save(test_edit)
    test_edit.id = saved_test_edit.id

    assert test_edit == saved_test_edit


def test_save_not_existing_test_result(sessionmaker_fixture):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = TestEdit(
        id=0,
        test_id=10,
        edit_type=EditTypes.COMPARISON_SETTINGS,
        created_at=datetime.datetime.now(),
        old_value={"key": "value"},
        new_value={"key": "new value"},
    )

    with pytest.raises(IntegrityError):
        repository.save(test_edit)


def test_find_by_test_id_should_find_empty_list(sessionmaker_fixture):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)

    result = repository.find_by_test_id(1)

    assert result == []


def test_find_by_test_id(sessionmaker_fixture, test_result):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edits = [
        TestEdit(
            id=0,
            test_id=test_result.id,
            edit_type=EditTypes.COMPARISON_SETTINGS,
            created_at=datetime.datetime.now(),
            old_value={"key": "value"},
            new_value={"key": "new value"},
        )
        for _ in range(10)
    ]
    repository.insert_many(test_edits)
    test_result_id = test_result.id
    test_result.id = 0
    test_result = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(test_result)
    repository.save(
        TestEdit(
            id=0,
            test_id=test_result.id,
            edit_type=EditTypes.COMPARISON_SETTINGS,
            created_at=datetime.datetime.now(),
            old_value={"key": "value"},
            new_value={"key": "new value"},
        )
    )

    results = repository.find_by_test_id(test_result_id)

    assert len(results) == 10
    for i, test_edit in enumerate(test_edits):
        test_edit.id = i + 1
        assert test_edit == results[i]


def test_find_by_test_id_with_edit_type(test_result, sessionmaker_fixture):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = TestEdit(
        id=0,
        test_id=test_result.id,
        edit_type=EditTypes.COMPARISON_SETTINGS,
        created_at=datetime.datetime.now(),
        old_value={"key": "value"},
        new_value={"key": "new value"},
    )
    saved_test_edit = repository.save(test_edit)
    other_test_edit = TestEdit(
        id=0,
        test_id=test_result.id,
        edit_type=EditTypes.REFERENCE_IMAGE,
        created_at=datetime.datetime.now(),
        old_value={"key": "value"},
        new_value={"key": "new value"},
    )
    repository.save(other_test_edit)

    results = repository.find_by_test_id(
        test_result.id, edit_type=EditTypes.COMPARISON_SETTINGS
    )

    assert results == [saved_test_edit]


def test_find_by_run_id_should_find_empty_list(sessionmaker_fixture, run):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)

    result = repository.find_by_run_id(run.id)

    assert result == []


def test_find_by_run_id_should_find(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestEditRepository(sessionmaker_fixture)
    test_edit = TestEdit(
        id=0,
        test_id=test_result.id,
        edit_type=EditTypes.COMPARISON_SETTINGS,
        created_at=datetime.datetime.now(),
        old_value={"key": "value"},
        new_value={"key": "new value"},
    )
    saved_test_edit = repository.save(test_edit)

    result = repository.find_by_run_id(run.id)

    assert result == [saved_test_edit]
