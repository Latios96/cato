import datetime
import os

import humanfriendly

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration


def test_create_default_config():
    configuration_default = AppConfigurationDefaults()

    config = configuration_default.create()

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        storage_configuration=StorageConfiguration(
            database_url="db_url", file_storage_url="file_storage_url"
        ),
        logging_configuration=LoggingConfiguration(
            "log.txt", True, humanfriendly.parse_size("10mb"), 10
        ),
        scheduler_configuration=SchedulerConfiguration(),
        sentry_configuration=SentryConfiguration.default(),
        session_configuration=SessionConfiguration.default(),
    )


def test_create_default_config_ready_to_use():
    configuration_default = AppConfigurationDefaults()

    config = configuration_default.create_ready_to_use("a/path/to/a/config/folder")

    assert config == AppConfiguration(
        port=5000,
        debug=False,
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
    )
