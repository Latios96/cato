import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.sqlalchemy.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
    _SessionMapping,
)


def test_insert_session(sqlalchemy_session_repository, auth_user):
    session = Session(
        id=SessionId.none(),
        user_id=auth_user.id,
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now(),
    )

    saved_session = sqlalchemy_session_repository.save(session)

    session.id = saved_session.id
    assert saved_session.id != SessionId.none()
    assert session == saved_session


def test_find_by_id(sqlalchemy_session_repository, auth_user):
    session = Session(
        id=SessionId.none(),
        user_id=auth_user.id,
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now(),
    )
    saved_session = sqlalchemy_session_repository.save(session)

    found_session = sqlalchemy_session_repository.find_by_id(saved_session.id)

    assert found_session == saved_session


def test_delete_by_id(sqlalchemy_session_repository, auth_user):
    session = Session(
        id=SessionId.none(),
        user_id=auth_user.id,
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now(),
    )
    saved_session = sqlalchemy_session_repository.save(session)

    sqlalchemy_session_repository.delete_by_id(saved_session.id)

    assert sqlalchemy_session_repository.find_by_id(saved_session.id) is None


def test_update_session(sqlalchemy_session_repository, auth_user):
    session = Session(
        id=SessionId.none(),
        user_id=auth_user.id,
        created_at=datetime.datetime.now(),
        expires_at=datetime.datetime.now(),
    )
    session = sqlalchemy_session_repository.save(session)
    new_expires_at = datetime.datetime(year=2020, month=10, day=1)

    session.expires_at = new_expires_at
    session = sqlalchemy_session_repository.save(session)
    loaded_session = sqlalchemy_session_repository.find_by_id(session.id)

    assert loaded_session.expires_at == new_expires_at


class TestFindExpiredSessions:
    def test_find_by_expires_at_is_older_than_should_return_empty_list_for_empty_table(
        self, sqlalchemy_session_repository, auth_user
    ):
        results = sqlalchemy_session_repository.find_by_expires_at_is_older_than(
            datetime.datetime.now()
        )

        assert results == []

    def test_find_by_expires_at_is_older_than_should_not_return_not_expired_sessions(
        self, sqlalchemy_session_repository, auth_user
    ):
        session = Session(
            id=SessionId.none(),
            user_id=auth_user.id,
            created_at=datetime.datetime(year=2020, month=10, day=1),
            expires_at=datetime.datetime(year=2020, month=10, day=2),
        )
        sqlalchemy_session_repository.save(session)

        results = sqlalchemy_session_repository.find_by_expires_at_is_older_than(
            datetime.datetime(year=2020, month=10, day=1)
        )

        assert results == []

    def test_find_by_expires_at_is_older_than_should_not_return_not_expired_sessions_with_same_datetime(
        self, sqlalchemy_session_repository, auth_user
    ):
        session = Session(
            id=SessionId.none(),
            user_id=auth_user.id,
            created_at=datetime.datetime(year=2020, month=10, day=1),
            expires_at=datetime.datetime(year=2020, month=10, day=2),
        )
        sqlalchemy_session_repository.save(session)

        results = sqlalchemy_session_repository.find_by_expires_at_is_older_than(
            datetime.datetime(year=2020, month=10, day=2)
        )

        assert results == []

    def test_find_by_expires_at_is_older_than_should_not_return_expired_sessions(
        self, sqlalchemy_session_repository, auth_user
    ):
        session = Session(
            id=SessionId.none(),
            user_id=auth_user.id,
            created_at=datetime.datetime(year=2020, month=10, day=1),
            expires_at=datetime.datetime(year=2020, month=10, day=2),
        )
        saved_session = sqlalchemy_session_repository.save(session)

        results = sqlalchemy_session_repository.find_by_expires_at_is_older_than(
            datetime.datetime(year=2020, month=10, day=3)
        )

        assert results == [saved_session]


class TestConstraints:
    def test_inserting_session_token_duplicate_should_raise_error(
        self, sessionmaker_fixture, auth_user
    ):
        session = sessionmaker_fixture()
        session_id = str(SessionId.generate())
        auth_session1 = _SessionMapping(
            id=session_id,
            user_id=auth_user.id,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )
        auth_session2 = _SessionMapping(
            id=session_id,
            user_id=auth_user.id,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )
        session.add(auth_session1)
        session.commit()

        with pytest.raises(IntegrityError):
            session.add(auth_session2)
            session.commit()

    @pytest.mark.parametrize(
        "session_mapping",
        [
            _SessionMapping(
                id=None,
                user_id=1,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now(),
            ),
            _SessionMapping(
                id=str(SessionId.generate()),
                user_id=None,
                created_at=datetime.datetime.now(),
                expires_at=datetime.datetime.now(),
            ),
            _SessionMapping(
                id=str(SessionId.generate()),
                user_id=1,
                created_at=None,
                expires_at=datetime.datetime.now(),
            ),
            _SessionMapping(
                id=str(SessionId.generate()),
                user_id=1,
                created_at=datetime.datetime.now(),
                expires_at=None,
            ),
        ],
    )
    def test_insert_nulls_for_non_nullable_fields_should_fail(
        self, session_mapping, auth_user, sessionmaker_fixture
    ):
        session = sessionmaker_fixture()

        with pytest.raises(IntegrityError):
            session.add(session_mapping)
            session.commit()

    def test_inserting_not_existing_user_id_should_not_work(
        self, sqlalchemy_session_repository
    ):
        session = Session(
            id=SessionId.none(),
            user_id=42,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )

        with pytest.raises(IntegrityError):
            sqlalchemy_session_repository.save(session)
