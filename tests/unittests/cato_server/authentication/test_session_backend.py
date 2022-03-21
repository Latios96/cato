import datetime
from typing import Tuple

import pytest
from freezegun import freeze_time

from cato_server.authentication.session_backend import SessionBackend
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.domain.auth.auth_user import AuthUser
from cato_common.domain.auth.email import Email
from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_common.domain.auth.username import Username
from cato_server.storage.abstract.session_repository import SessionRepository
from tests.utils import mock_safe


@pytest.fixture
def session_backend_fixture() -> Tuple[SessionBackend, SessionRepository]:
    mock_session_repository = mock_safe(SessionRepository)
    session_backend = SessionBackend(
        mock_session_repository,
        SessionConfiguration.default(),
    )
    yield session_backend, mock_session_repository


class TestGetSession:
    def test_get_session_should_return_none_if_no_session_exists_for_id(
        self, session_backend_fixture
    ):
        session_backend, mock_session_repository = session_backend_fixture
        mock_session_repository.find_by_id.return_value = None

        session = session_backend.get_session(SessionId.generate())

        assert session is None

    @freeze_time(datetime.datetime(2022, 1, 29, 1, 0))
    def test_session_session_should_return_not_expired_session(
        self, session_backend_fixture
    ):
        session_backend, mock_session_repository = session_backend_fixture
        created_at = datetime.datetime(year=2022, month=1, day=29, hour=0, minute=0)
        expires_at = datetime.datetime(year=2022, month=1, day=29, hour=2, minute=0)
        session = Session(
            id=SessionId.generate(),
            user_id=1,
            created_at=created_at,
            expires_at=expires_at,
        )
        mock_session_repository.find_by_id.return_value = session

        loaded_session = session_backend.get_session(SessionId.generate())

        assert loaded_session == session

    @freeze_time(datetime.datetime(2022, 1, 29, 2, 0, 0))
    def test_session_session_should_not_return_session_with_zero_remaining_time(
        self, session_backend_fixture
    ):
        session_backend, mock_session_repository = session_backend_fixture
        created_at = datetime.datetime(year=2022, month=1, day=29, hour=0, minute=0)
        expires_at = datetime.datetime(year=2022, month=1, day=29, hour=2, minute=0)
        session = Session(
            id=SessionId.generate(),
            user_id=1,
            created_at=created_at,
            expires_at=expires_at,
        )
        mock_session_repository.find_by_id.return_value = session

        loaded_session = session_backend.get_session(SessionId.generate())

        assert loaded_session is None

    @freeze_time(datetime.datetime(2022, 3, 29, 2, 0, 0))
    def test_session_session_should_not_return_expired_session(
        self, session_backend_fixture
    ):
        session_backend, mock_session_repository = session_backend_fixture
        created_at = datetime.datetime(year=2022, month=1, day=29, hour=0, minute=0)
        expires_at = datetime.datetime(year=2022, month=1, day=29, hour=2, minute=0)
        session = Session(
            id=SessionId.generate(),
            user_id=1,
            created_at=created_at,
            expires_at=expires_at,
        )
        mock_session_repository.find_by_id.return_value = session

        loaded_session = session_backend.get_session(SessionId.generate())

        assert loaded_session is None


def mock_save(session):
    session.id = SessionId("generated id")
    return session


@freeze_time(datetime.datetime(2022, 1, 29))
def test_create_session(session_backend_fixture):
    session_backend, mock_session_repository = session_backend_fixture
    mock_session_repository.save.side_effect = mock_save
    auth_user = AuthUser(
        id=1,
        username=Username("username"),
        fullname=Username("User Username"),
        email=Email("foo@bar.com"),
    )

    session = session_backend.create_session(auth_user)

    assert session == Session(
        id=SessionId("generated id"),
        user_id=1,
        created_at=datetime.datetime(2022, 1, 29),
        expires_at=datetime.datetime(2022, 1, 29, 2, 0, 0),
    )


class TestLogoutFromSession:
    def test_logout_successfully(self, session_backend_fixture):
        session_backend, mock_session_repository = session_backend_fixture
        session_id = SessionId.generate()
        session = Session(
            id=session_id,
            user_id=1,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )

        session_backend.logout_from_session(session)

        mock_session_repository.delete_by_id.assert_called_with(session_id)

    def test_logout_from_not_existing_session(self, session_backend_fixture):
        session_backend, mock_session_repository = session_backend_fixture
        mock_session_repository.delete_by_id.side_effect = ValueError()
        session_id = SessionId.generate()
        session = Session(
            id=session_id,
            user_id=1,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )

        session_backend.logout_from_session(session)

        mock_session_repository.delete_by_id.assert_called_with(session_id)
