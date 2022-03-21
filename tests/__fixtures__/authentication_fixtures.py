import json
from base64 import b64encode

import itsdangerous
import pytest

from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.session_backend import SessionBackend
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.session import Session
from cato_server.storage.sqlalchemy.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
)


@pytest.fixture
def http_session_factory(app_and_config_fixture, sessionmaker_fixture):
    app, config = app_and_config_fixture

    def factory(auth_user: AuthUser) -> Session:
        session_repository = SqlAlchemySessionRepository(sessionmaker_fixture)
        return SessionBackend(
            session_repository, config.session_configuration
        ).create_session(auth_user)

    return factory


@pytest.fixture
def http_session(http_session_factory, auth_user):
    return http_session_factory(auth_user)


@pytest.fixture
def http_session_cookie_factory(app_and_config_fixture):
    app, config = app_and_config_fixture

    def factory(session: Session):
        signer = itsdangerous.TimestampSigner(config.secret.get_secret_value())

        session_data = {"session_id": str(session.id)}
        data = b64encode(json.dumps(session_data).encode("utf-8"))
        data = signer.sign(data).decode("utf-8")
        return "session", data

    return factory


@pytest.fixture
def http_session_cookie(http_session_cookie_factory, http_session):
    return http_session_cookie_factory(http_session)


@pytest.fixture
def client_with_session(http_session_cookie, client):
    cookie_name, cookie_value = http_session_cookie
    client.cookies.set(cookie_name, cookie_value)
    return client


@pytest.fixture
def api_token_str():
    return ApiTokenStr(
        b"eyJuYW1lIjogInRlc3QiLCAiaWQiOiAiYWI1ZDIwMDA4YmIxZjI3YTE0NDJhNGRhMzk4YzAxNzEyYjQ4NThkMDYyMWJlZjA4NjAyYjc2ZjEwNGNlZjE2ZiIsICJjcmVhdGVkQXQiOiAiMjAyMi0wMy0yMVQxNzoxNToyNC4zMjg2MzMiLCAiZXhwaXJlc0F0IjogIjIwMjItMDMtMjFUMTk6MTU6MjQuMzI4NjMzIn0=.Yjikng.4DHH2-KIXCUigxgQHJ_W2My3IBw"
    )
