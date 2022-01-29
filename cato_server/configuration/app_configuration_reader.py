import configparser
import datetime

import os

import humanfriendly

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.scheduler_configuration import (
    SchedulerConfiguration,
    DeadlineSchedulerConfiguration,
)
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration

import logging

logger = logging.getLogger(__name__)


class AppConfigurationReader:
    def read_file(self, path: str) -> AppConfiguration:
        if not os.path.exists(path):
            raise ValueError(f"Supplied config path {path} does not exists!")

        config = configparser.ConfigParser()
        logger.info("Reading config from path %s..", path)
        config.read(path)

        storage_configuration = self._read_storage_configuration(config)
        logging_configuration = self._read_logging_configuration(config)
        scheduler_configuration = self._read_scheduler_configuration(config)
        sentry_configuration = self._read_sentry_configuration(config)
        session_configuration = self._read_session_configuration(config)

        return AppConfiguration(
            port=config.getint(
                "app", "port", fallback=AppConfigurationDefaults.PORT_DEFAULT
            ),
            debug=config.getboolean(
                "app", "debug", fallback=AppConfigurationDefaults.DEBUG_DEFAULT
            ),
            storage_configuration=storage_configuration,
            logging_configuration=logging_configuration,
            scheduler_configuration=scheduler_configuration,
            sentry_configuration=sentry_configuration,
            session_configuration=session_configuration,
        )

    def _read_storage_configuration(
        self, config: configparser.ConfigParser
    ) -> StorageConfiguration:
        return StorageConfiguration(
            database_url=config.get("storage", "database_url"),
            file_storage_url=config.get("storage", "file_storage_url"),
        )

    def _read_logging_configuration(
        self, config: configparser.ConfigParser
    ) -> LoggingConfiguration:
        max_bytes_str = config.get("logging", "max_file_size", fallback=None)
        if max_bytes_str:
            max_bytes = humanfriendly.parse_size(max_bytes_str)
        else:
            max_bytes = AppConfigurationDefaults.MAX_BYTES_DEFAULT
        return LoggingConfiguration(
            log_file_path=config.get("logging", "log_file_path", fallback="log.txt"),
            use_file_handler=config.getboolean(
                "logging",
                "use_file_handler",
                fallback=AppConfigurationDefaults.USE_FILE_HANDLER_DEFAULT,
            ),
            max_bytes=max_bytes,
            backup_count=config.getint(
                "logging",
                "backup_count",
                fallback=AppConfigurationDefaults.BACKUP_COUNT_DEFAULT,
            ),
        )

    def _read_scheduler_configuration(self, config):
        name = config.get("scheduler", "name", fallback=None)
        if not name or name == "None":
            return SchedulerConfiguration()
        if name == "Deadline":
            url = config.get(
                "scheduler", "deadline_url", fallback="http://localhost:8082"
            )
            return DeadlineSchedulerConfiguration(url)

    def _read_sentry_configuration(self, config):
        sentry_url = config.get("sentry", "url", fallback=None)
        return SentryConfiguration(url=sentry_url)

    def _read_session_configuration(self, config):
        session_lifetime_str = config.get("session", "lifetime", fallback=None)
        if not session_lifetime_str:
            return SessionConfiguration(lifetime=datetime.timedelta(hours=2))
        session_lifetime_seconds = humanfriendly.parse_timespan(session_lifetime_str)
        session_lifetime = datetime.timedelta(seconds=session_lifetime_seconds)
        return SessionConfiguration(lifetime=session_lifetime)
