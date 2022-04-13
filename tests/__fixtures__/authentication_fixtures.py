import datetime
import json
import os
import secrets
from base64 import b64encode
from typing import Dict, Optional

import itsdangerous
import pytest
from itsdangerous import URLSafeSerializer
from starlette.requests import Request
from starlette_csrf import CSRFMiddleware

from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_server.authentication.api_token_signer import ApiTokenSigner
from cato_server.authentication.session_backend import SessionBackend
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.secrets_configuration import SecretsConfiguration
from cato_server.domain.auth.api_token import ApiToken
from cato_server.domain.auth.auth_user import AuthUser
from cato_server.domain.auth.secret_str import SecretStr
from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.sqlalchemy.sqlalchemy_session_repository import (
    SqlAlchemySessionRepository,
)
from dateutil.parser import parse

from cato_server.utils.datetime_utils import aware_now_in_utc


@pytest.fixture
def http_session_factory(app_and_config_fixture, sqlalchemy_session_repository):
    app, config = app_and_config_fixture

    def factory(auth_user: AuthUser) -> Session:
        return SessionBackend(
            sqlalchemy_session_repository, config.session_configuration
        ).create_session(auth_user)

    return factory


@pytest.fixture
def http_session(http_session_factory, auth_user):
    return http_session_factory(auth_user)


@pytest.fixture
def http_session_cookie_factory(app_and_config_fixture):
    app, config = app_and_config_fixture

    def factory(session: Session):
        signer = itsdangerous.TimestampSigner(
            config.secrets_configuration.sessions_secret.get_secret_value()
        )

        session_data = {"session_id": str(session.id)}
        data = b64encode(json.dumps(session_data).encode("utf-8"))
        data = signer.sign(data).decode("utf-8")
        return "session", data

    return factory


@pytest.fixture
def http_session_cookie(http_session_cookie_factory, http_session):
    return http_session_cookie_factory(http_session)


@pytest.fixture
def crsf_token_factory(app_and_config_fixture):
    app, config = app_and_config_fixture

    def factory():
        return CSRFMiddleware(
            None, config.secrets_configuration.csrf_secret.get_secret_value()
        )._generate_csrf_token()

    return factory


@pytest.fixture
def crsf_token(crsf_token_factory):
    return crsf_token_factory()


@pytest.fixture
def client_with_session(http_session_cookie, crsf_token, client):
    cookie_name, cookie_value = http_session_cookie
    client.cookies.set(cookie_name, cookie_value)
    client.cookies.set("XSRF-TOKEN", crsf_token)
    client.headers["X-XSRF-TOKEN"] = crsf_token
    return client


@pytest.fixture
def fixed_http_session():
    created_at = aware_now_in_utc()
    expires_at = created_at + datetime.timedelta(hours=2)
    return Session(
        id=SessionId("qfq0kpmAKSz2mXqr2AsI8hoN-oVrvovk9nxnIG6MpMM"),
        user_id=1,
        created_at=created_at,
        expires_at=expires_at,
    )


@pytest.fixture
def fixed_api_token():
    return ApiToken(
        name=ApiTokenName("test"),
        id=ApiTokenId(
            "ab5d20008bb1f27a1442a4da398c01712b4858d0621bef08602b76f104cef16f"
        ),
        created_at=parse("2022-03-21T17:15:24.328633"),
        expires_at=parse("2022-03-21T19:15:24.328633"),
    )


@pytest.fixture
def fixed_api_token_str():
    return ApiTokenStr(
        b"eyJuYW1lIjogInRlc3QiLCAiaWQiOiAiYWI1ZDIwMDA4YmIxZjI3YTE0NDJhNGRhMzk4YzAxNzEyYjQ4NThkMDYyMWJlZjA4NjAyYjc2ZjEwNGNlZjE2ZiIsICJjcmVhdGVkQXQiOiAiMjAyMi0wMy0yMVQxNzoxNToyNC4zMjg2MzMiLCAiZXhwaXJlc0F0IjogIjIwMjItMDMtMjFUMTk6MTU6MjQuMzI4NjMzIn0=.Yjikng.4DHH2-KIXCUigxgQHJ_W2My3IBw"
    )


@pytest.fixture
def api_token_str_factory(app_and_config_fixture, object_mapper):
    def factory(
        name=ApiTokenName("test"),
        id=ApiTokenId.generate(),
        created_at=None,
        expires_at=None,
        secret: SecretStr = None,
    ):
        if not created_at:
            created_at = aware_now_in_utc()
        if not expires_at:
            expires_at = created_at + datetime.timedelta(hours=2)

        if not secret:
            secrets_config = app_and_config_fixture[1].secrets_configuration
        else:
            secrets_config = SecretsConfiguration.default()
            secrets_config.api_tokens_secret = secret

        api_token_signer = ApiTokenSigner(object_mapper, secrets_config)

        api_token = ApiToken(
            name=name,
            id=id,
            created_at=created_at,
            expires_at=expires_at,
        )
        return api_token_signer.sign(api_token)

    return factory


@pytest.fixture
def api_token_str(api_token_str_factory):
    return api_token_str_factory()


@pytest.fixture
def env_with_api_token(api_token_str):
    env_copy = os.environ.copy()
    env_copy["CATO_API_TOKEN"] = str(api_token_str)
    return env_copy


@pytest.fixture
def request_factory():
    def factory(
        route: str,
        session_dict: Optional[Dict[str, str]] = None,
        auth_header: Optional[bytes] = None,
    ):
        headers = [
            (b"host", b"localhost:5000"),
            (b"connection", b"keep-alive"),
            (
                b"sec-ch-ua",
                b'" Not A;Brand";v="99", "Chromium";v="99", "Google Chrome";v="99"',
            ),
            (b"sec-ch-ua-mobile", b"?0"),
            (b"sec-ch-ua-platform", b'"Windows"'),
            (b"upgrade-insecure-requests", b"1"),
            (
                b"user-agent",
                b"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36",
            ),
            (
                b"accept",
                b"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            ),
            (b"sec-fetch-site", b"none"),
            (b"sec-fetch-mode", b"navigate"),
            (b"sec-fetch-user", b"?1"),
            (b"sec-fetch-dest", b"document"),
            (b"accept-encoding", b"gzip, deflate, br"),
            (b"accept-language", b"de-DE,de;q=0.9,en;q=0.8,en-US;q=0.7"),
        ]
        if auth_header:
            headers.append((b"authorization", auth_header))

        scope = {
            "type": "http",
            "asgi": {"version": "3.0", "spec_version": "2.1"},
            "http_version": "1.1",
            "server": ("::1", 5000),
            "client": ("::1", 55149),
            "scheme": "http",
            "method": "GET",
            "root_path": "",
            "path": route,
            "raw_path": route,
            "query_string": b"",
            "headers": headers,
            "state": {},
        }
        if not session_dict:
            session_dict = {}
        scope["session"] = session_dict

        return Request(scope)

    return factory
