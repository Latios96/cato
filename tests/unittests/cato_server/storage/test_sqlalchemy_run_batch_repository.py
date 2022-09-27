import uuid

import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.run_batch_identifier import RunBatchIdentifier
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName
from tests.unittests.cato_server.storage.conftest import sqltap_query_count_asserter


class TestSave:
    def test_should_save_to_database(
        self, sqlalchemy_run_batch_repository, run_batch_factory
    ):
        run_batch = run_batch_factory()

        saved_run_batch = sqlalchemy_run_batch_repository.save(run_batch)

        run_batch.id = 1
        assert saved_run_batch == run_batch

    def test_should_also_save_runs_to_database(
        self, sqlalchemy_run_batch_repository, run_batch_factory, run_factory
    ):
        run_batch = run_batch_factory(runs=[run_factory()])

        saved_run_batch = sqlalchemy_run_batch_repository.save(run_batch)

        run_batch.id = 1
        assert saved_run_batch.runs[0].id == 1

    def test_should_not_save_duplicated_run_batch_identifier(
        self, sqlalchemy_run_batch_repository, run_batch_factory
    ):
        run_batch = run_batch_factory()

        sqlalchemy_run_batch_repository.save(run_batch)
        with pytest.raises(IntegrityError):
            sqlalchemy_run_batch_repository.save(run_batch)

    def test_should_not_save_multiple_runs_with_different_identifiers(
        self, sqlalchemy_run_batch_repository, run_batch_factory
    ):
        run_batch_1 = run_batch_factory()
        run_batch_2 = run_batch_factory(
            RunBatchIdentifier(
                provider=RunBatchProvider.LOCAL_COMPUTER,
                run_name=RunName("mac-os"),
                run_identifier=RunIdentifier("3046812908-2"),
            )
        )

        sqlalchemy_run_batch_repository.save(run_batch_1)
        sqlalchemy_run_batch_repository.save(run_batch_2)

    def test_should_not_save_multiple_runs_with_different_project_ids(
        self, sqlalchemy_run_batch_repository, run_batch_factory, saving_project_factory
    ):
        run_batch_1 = run_batch_factory()
        run_batch_2 = run_batch_factory(
            project_id=saving_project_factory(name="other_project").id
        )

        sqlalchemy_run_batch_repository.save(run_batch_1)
        sqlalchemy_run_batch_repository.save(run_batch_2)


def test_find_by_project_id_and_run_batch_identifier_should_find_correct_one(
    sqlalchemy_run_batch_repository,
    run_batch,
    saving_run_batch_factory,
    saving_project_factory,
):
    for i in range(10):
        run_identifier = RunIdentifier.random()
        run_batch_identifier = run_batch.run_batch_identifier.copy(
            run_identifier=run_identifier
        )
        saving_run_batch_factory(run_batch_identifier=run_batch_identifier)
    for i in range(10):
        run_identifier = RunIdentifier.random()
        run_batch_identifier = run_batch.run_batch_identifier.copy(
            run_identifier=run_identifier
        )
        saving_run_batch_factory(
            run_batch_identifier=run_batch_identifier,
            project_id=saving_project_factory(name=str(uuid.uuid4())).id,
        )

    found_run_batch = (
        sqlalchemy_run_batch_repository.find_by_project_id_and_run_batch_identifier(
            run_batch.project_id, run_batch.run_batch_identifier
        )
    )

    assert found_run_batch == run_batch


class TestDontUseTooManyQueries:
    def test_find_by_id_should_not_use_too_many_queries(
        self,
        sqlalchemy_run_batch_repository,
        saving_run_batch_factory,
        run_factory,
        run_batch_identifier,
    ):
        run_batch = saving_run_batch_factory(
            runs=[run_factory(run_batch_id=0) for x in range(5)]
        )

        with sqltap_query_count_asserter(1):
            sqlalchemy_run_batch_repository.find_by_id(run_batch.id)

    def test_find_by_project_id_and_run_batch_identifier_should_not_use_too_many_queries(
        self,
        sqlalchemy_run_batch_repository,
        saving_run_batch_factory,
        run_factory,
        run_batch_identifier,
    ):
        run_batch = saving_run_batch_factory(
            runs=[run_factory(run_batch_id=0) for x in range(5)]
        )

        with sqltap_query_count_asserter(1):
            sqlalchemy_run_batch_repository.find_by_project_id_and_run_batch_identifier(
                run_batch.project_id, run_batch.run_batch_identifier
            )

    def test_find_or_save_by_project_id_and_run_batch_identifier_should_not_use_too_many_queries(
        self,
        sqlalchemy_run_batch_repository,
        saving_run_batch_factory,
        run_factory,
        run_batch_identifier,
    ):
        run_batch = saving_run_batch_factory(
            runs=[run_factory(run_batch_id=0) for x in range(5)]
        )

        with sqltap_query_count_asserter(1):
            sqlalchemy_run_batch_repository.find_or_save_by_project_id_and_run_batch_identifier(
                run_batch.project_id, run_batch.run_batch_identifier, lambda: None
            )


def test_find_by_project_id_and_run_batch_identifier_should_not_find_with_different_identifier(
    sqlalchemy_run_batch_repository, run_batch
):
    run_batch_identifier = run_batch.run_batch_identifier.copy(
        run_identifier=RunIdentifier("3046812908-2")
    )
    found_run_batch = (
        sqlalchemy_run_batch_repository.find_by_project_id_and_run_batch_identifier(
            run_batch.project_id, run_batch_identifier
        )
    )

    assert found_run_batch is None


def test_find_by_project_id_and_run_batch_identifier_should_not_find_with_different_project_id(
    sqlalchemy_run_batch_repository, run_batch
):
    found_run_batch = (
        sqlalchemy_run_batch_repository.find_by_project_id_and_run_batch_identifier(
            42, run_batch.run_batch_identifier
        )
    )

    assert found_run_batch is None


def test_find_or_save_by_project_id_and_run_batch_identifier_should_create(
    sqlalchemy_run_batch_repository, run_batch_factory, project
):
    run_batch = run_batch_factory()
    saved_run_batch = sqlalchemy_run_batch_repository.find_or_save_by_project_id_and_run_batch_identifier(
        project.id, run_batch.run_batch_identifier, lambda: run_batch
    )

    run_batch.id = 1
    assert saved_run_batch == run_batch


def test_find_or_save_by_project_id_and_run_batch_identifier_should_find(
    sqlalchemy_run_batch_repository, run_batch
):
    found_run_batch = sqlalchemy_run_batch_repository.find_or_save_by_project_id_and_run_batch_identifier(
        run_batch.project_id, run_batch.run_batch_identifier, lambda: run_batch
    )

    assert found_run_batch == run_batch