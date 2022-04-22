import contextlib
from contextvars import ContextVar
from typing import Optional, Callable

from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


class SessionAlreadyInitializedException(Exception):
    def __init__(self):
        super(SessionAlreadyInitializedException, self).__init__(
            "A session was already initialized for this context."
        )


class NoSessionInitializedException(Exception):
    def __init__(self):
        super(NoSessionInitializedException, self).__init__(
            "No session was initialized for this context. Please initialize a session first."
        )


class SessionProvider:
    def __init__(self, session_maker: Callable[[], Session]):
        self._session_maker = session_maker
        self._session_context: ContextVar[Optional[Session]] = ContextVar(
            "session_context", default=None
        )

    def init_session(self):
        if self._session_context.get() is not None:
            raise SessionAlreadyInitializedException()
        session = self._session_maker()
        self._session_context.set(session)
        return session

    def get_session(self) -> Session:
        session = self._session_context.get()
        if session is None:
            raise NoSessionInitializedException()
        return session

    def remove_session(self):
        session = self._session_context.get()
        if session is None:
            raise NoSessionInitializedException()
        self._session_context.set(None)


@contextlib.contextmanager
def within_transaction(session_provider: SessionProvider):
    session = session_provider.init_session()
    try:
        yield
        session.commit()
        session.close()
        session_provider.remove_session()
    except Exception as e:
        session.rollback()
        session.close()
        session_provider.remove_session()
        raise e
