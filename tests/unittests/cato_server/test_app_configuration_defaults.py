import os
from unittest import mock

import humanfriendly

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.parts.celery_configuration import CeleryConfiguration
from cato_server.configuration.parts.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.parts.oiio_configuration import OiioConfiguration
from cato_server.configuration.parts.scheduler_configuration import (
    SchedulerConfiguration,
)
from cato_server.configuration.parts.secrets_configuration import SecretsConfiguration
from cato_server.configuration.parts.sentry_configuration import SentryConfiguration
from cato_server.configuration.parts.session_configuration import SessionConfiguration
from cato_server.configuration.parts.storage_configuration import StorageConfiguration
from cato_server.domain.auth.secret_str import SecretStr


@mock.patch("secrets.token_urlsafe")
def test_create_default_config(mock_secrets_token_urlsafe):
    mock_secrets_token_urlsafe.return_value = "SECRET"
    configuration_default = AppConfigurationDefaults()

    config = configuration_default.create()

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        secrets_configuration=SecretsConfiguration(
            SecretStr("SECRET"), SecretStr("SECRET"), SecretStr("SECRET")
        ),
        hostname="localhost",
        public_url="http://127.0.0.1",
        workers=16,
        storage_configuration=StorageConfiguration(
            database_url="db_url", file_storage_url="file_storage_url"
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", True, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
        celery_configuration=CeleryConfiguration(
            broker_url="pyamqp://guest@localhost//"
        ),
        oiio_configuration=OiioConfiguration(thread_count=1),
    )


@mock.patch("secrets.token_urlsafe")
def test_create_default_config_ready_to_use(mock_secrets_token_urlsafe):
    mock_secrets_token_urlsafe.return_value = "SECRET"
    configuration_default = AppConfigurationDefaults()

    config = configuration_default.create_ready_to_use("a/path/to/a/config/folder")

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        secrets_configuration=SecretsConfiguration(
            SecretStr("SECRET"), SecretStr("SECRET"), SecretStr("SECRET")
        ),
        hostname="localhost",
        public_url="http://127.0.0.1",
        workers=16,
        storage_configuration=StorageConfiguration(
            database_url="sqlite:///{}".format(
                os.path.join("a/path/to/a/config/folder", "cato.db")
            ),
            file_storage_url=os.path.join("a/path/to/a/config/folder", "file_storage"),
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", True, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
        celery_configuration=CeleryConfiguration(
            broker_url="pyamqp://guest@localhost//"
        ),
        oiio_configuration=OiioConfiguration(thread_count=1),
    )
