import configparser
import datetime
import os

import humanfriendly
import pytest

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.scheduler_configuration import (
    SchedulerConfiguration,
    DeadlineSchedulerConfiguration,
)
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.domain.auth.secret_str import SecretStr

VALID_INI_FILE = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[scheduler]
name=None
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_DATABASE_URL = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_FILE_STORAGE_URL = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_DEBUG = """[app]
port=5000
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_SECRET = """[app]
port=5000
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_HOSTNAME = """[app]
port=5000
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

MISSING_OIDC_CLIENT_ID = """[app]
port=5000
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_secret=secret
well_known_url=http://somewhere"""

MISSING_OIDC_SECRET = """[app]
port=5000
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
well_known_url=http://somewhere"""

MISSING_OIDC_WELL_KNOWN_URL = """[app]
port=5000
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

WITH_LOGGING = """[app]
port=5000
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[logging]
log_file_path=cato-log.txt
use_file_handler=False
max_file_size=100mb
backup_count=100
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

WITH_LOGGING_INVALID_USE_FILE_HANDLER = """[app]
port=5000
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[logging]
use_file_handler=wurst
max_file_size=100mb
backup_count=100
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

WITH_LOGGING_INVALID_MAX_FILE_SIZE = """[app]
port=5000
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[logging]
use_file_handler=True
max_file_size=100wurst
backup_count=100
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

WITH_LOGGING_INVALID_BACKUP_COUNT = """[app]
port=5000
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[logging]
use_file_handler=True
max_file_size=1mb
backup_count=wurst
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""

WITH_DEADLINE_SCHEDULER_NO_URL = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[scheduler]
name=Deadline
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere
"""

WITH_DEADLINE_SCHEDULER_WITH_URL = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[scheduler]
name=Deadline
deadline_url=http://localhost:8085
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere
"""

WITH_SESSION_LIFETIME = """[app]
port=5000
debug=True
secret=SECRET
public_hostname=http://127.0.0.1
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url
[session]
lifetime=1h
[oidc]
client_id=client-id
client_secret=secret
well_known_url=http://somewhere"""


@pytest.fixture
def ini_file_creator(tmp_path):
    def create_ini_file(content):
        ini_path = os.path.join(str(tmp_path), "config.ini")
        with open(ini_path, "w") as f:
            f.write(content)
        return ini_path

    return create_ini_file


def test_read_not_existing_ini_file():
    reader = AppConfigurationReader()
    with pytest.raises(ValueError):
        reader.read_file("ini_path")


def test_read_valid_file(ini_file_creator):
    ini_path = ini_file_creator(VALID_INI_FILE)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=True,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
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
    )


def test_read_missing_debug_should_default_to_false(ini_file_creator):
    ini_path = ini_file_creator(MISSING_DEBUG)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
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
    )


def test_read_with_logging(ini_file_creator):
    ini_path = ini_file_creator(WITH_LOGGING)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
        logging_configuration=LoggingConfiguration(
            "cato-log.txt", False, humanfriendly.parse_size("100mb"), 100
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
    )


@pytest.mark.parametrize(
    "invalid_config,exception",
    [
        (WITH_LOGGING_INVALID_USE_FILE_HANDLER, ValueError),
        (WITH_LOGGING_INVALID_MAX_FILE_SIZE, humanfriendly.InvalidSize),
        (WITH_LOGGING_INVALID_BACKUP_COUNT, ValueError),
        (MISSING_DATABASE_URL, configparser.NoOptionError),
        (MISSING_FILE_STORAGE_URL, configparser.NoOptionError),
        (MISSING_SECRET, configparser.NoOptionError),
        (MISSING_HOSTNAME, configparser.NoOptionError),
        (MISSING_OIDC_CLIENT_ID, configparser.NoOptionError),
        (MISSING_OIDC_SECRET, configparser.NoOptionError),
        (MISSING_OIDC_WELL_KNOWN_URL, configparser.NoOptionError),
    ],
)
def test_read_missing_should_fail(invalid_config, exception, ini_file_creator):
    ini_path = ini_file_creator(invalid_config)
    reader = AppConfigurationReader()

    with pytest.raises(exception):
        reader.read_file(ini_path)


def test_read_scheduler_with_deadline_should_use_default_url(ini_file_creator):
    ini_path = ini_file_creator(WITH_DEADLINE_SCHEDULER_NO_URL)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=True,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
        logging_configuration=LoggingConfiguration("log.txt", True, 10000000, 10),
        scheduler_configuration=DeadlineSchedulerConfiguration(
            url="http://localhost:8082"
        ),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
    )


def test_read_scheduler_with_deadline_should_use_provided_url(ini_file_creator):
    ini_path = ini_file_creator(WITH_DEADLINE_SCHEDULER_WITH_URL)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=True,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
        logging_configuration=LoggingConfiguration("log.txt", True, 10000000, 10),
        scheduler_configuration=DeadlineSchedulerConfiguration(
            url="http://localhost:8085"
        ),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
    )


def test_read_with_session_lifetime(ini_file_creator):
    ini_path = ini_file_creator(WITH_SESSION_LIFETIME)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=True,
        secret=SecretStr("SECRET"),
        public_hostname="http://127.0.0.1",
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", True, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration(
            lifetime=datetime.timedelta(hours=1)
        ),
        oidc_configuration=OidcConfiguration(
            client_id="client-id",
            client_secret=SecretStr("secret"),
            well_known_url="http://somewhere",
        ),
    )
