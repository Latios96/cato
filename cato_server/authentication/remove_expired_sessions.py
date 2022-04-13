import logging

from cato_server.storage.abstract.session_repository import SessionRepository
from cato_server.utils.datetime_utils import aware_now_in_utc

logger = logging.getLogger(__name__)


class RemoveExpiredSessions:
    def __init__(self, session_repository: SessionRepository):
        self._session_repository = session_repository

    def remove_expired_sessions(self):
        logger.info("Checking for expired sessions..")
        expired_sessions = self._session_repository.find_by_expires_at_is_older_than(
            aware_now_in_utc()
        )

        if not expired_sessions:
            logger.info("No sessions to remove")
            return

        for expired_session in expired_sessions:
            self._session_repository.delete_by_id(expired_session.id)

        logger.info("Removed %s expired sessions", len(expired_sessions))
