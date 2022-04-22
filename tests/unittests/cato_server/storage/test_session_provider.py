import pytest

from cato_common.domain.project import Project
from cato_server.storage.sqlalchemy.session_provider import (
    SessionAlreadyInitializedException,
    NoSessionInitializedException,
    within_transaction,
)
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)


class TestSessionProvider:
    def test_init_session_success(self, session_provider):
        session = session_provider.init_session()

        assert session is not None

    def test_init_session_should_fail_if_there_is_already_a_session(
        self, session_provider
    ):
        session_provider.init_session()
        with pytest.raises(SessionAlreadyInitializedException):
            session_provider.init_session()

    def test_get_session_success(self, session_provider):
        created_session = session_provider.init_session()
        session = session_provider.get_session()

        assert session is not None and session is created_session

    def test_get_session_should_fail_if_no_session_was_initialized(
        self, session_provider
    ):
        with pytest.raises(NoSessionInitializedException):
            session_provider.get_session()

    def test_remove_session_success(self, session_provider):
        session_provider.init_session()

        session_provider.remove_session()

        with pytest.raises(NoSessionInitializedException):
            session_provider.get_session()

    def test_remove_session_should_fail_if_there_is_no_session_to_remove(
        self, session_provider
    ):
        with pytest.raises(NoSessionInitializedException):
            session_provider.remove_session()


class TestWithinTransaction:
    def test_within_transaction_commits(
        self,
        session_provider,
    ):
        with within_transaction(session_provider):
            project = SqlAlchemyProjectRepository(session_provider).save(
                Project(id=0, name="test")
            )

        with within_transaction(session_provider):
            assert (
                SqlAlchemyProjectRepository(session_provider).find_by_id(project.id)
                == project
            )

    def test_within_transaction_rolls_back_and_raises(self, session_provider):
        with pytest.raises(ValueError):
            with within_transaction(session_provider):
                project = SqlAlchemyProjectRepository(session_provider).save(
                    Project(id=0, name="test")
                )
                raise ValueError("test")

        with within_transaction(session_provider):
            assert (
                SqlAlchemyProjectRepository(session_provider).find_by_id(project.id)
                is None
            )
