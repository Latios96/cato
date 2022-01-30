import datetime

from cato_server.authentication.remove_expired_sessions import RemoveExpiredSessions
from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.abstract.session_repository import SessionRepository
from tests.utils import mock_safe


def test_should_pass_if_no_sessions_are_expired():
    mock_session_repository = mock_safe(SessionRepository)
    mock_session_repository.find_by_expires_at_is_older_than.return_value = []
    remove_expired_sessions = RemoveExpiredSessions(mock_session_repository)

    remove_expired_sessions.remove_expired_sessions()

    mock_session_repository.delete_by_id.assert_not_called()


def test_should_delete_expired_sessions():
    mock_session_repository = mock_safe(SessionRepository)
    session_id = SessionId.generate()
    mock_session_repository.find_by_expires_at_is_older_than.return_value = [
        Session(
            id=session_id,
            user_id=1,
            created_at=datetime.datetime.now(),
            expires_at=datetime.datetime.now(),
        )
    ]
    remove_expired_sessions = RemoveExpiredSessions(mock_session_repository)

    remove_expired_sessions.remove_expired_sessions()

    mock_session_repository.delete_by_id.assert_called_with(session_id)
