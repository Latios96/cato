import configparser
import logging
from typing import IO, cast

import humanfriendly

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.scheduler_configuration import (
    DeadlineSchedulerConfiguration,
)

logger = logging.getLogger(__name__)


class AppConfigurationWriter:
    def write_stream(self, config: AppConfiguration, stream: IO) -> None:
        config_writer = configparser.ConfigParser()
        config_writer.add_section("app")
        config_writer.add_section("secrets")
        config_writer.add_section("storage")
        config_writer.add_section("scheduler")
        config_writer.add_section("session")
        config_writer.add_section("oidc")
        config_writer.set("app", "port", str(config.port))
        config_writer.set("app", "debug", str(config.debug))
        config_writer.set("app", "hostname", config.hostname)
        config_writer.set("app", "public_url", config.public_url)
        config_writer.set(
            "secrets",
            "sessions_secret",
            config.secrets_configuration.sessions_secret.get_secret_value(),
        )
        config_writer.set(
            "secrets",
            "csrf_secret",
            config.secrets_configuration.csrf_secret.get_secret_value(),
        )
        config_writer.set(
            "secrets",
            "api_tokens_secret",
            config.secrets_configuration.api_tokens_secret.get_secret_value(),
        )
        config_writer.set(
            "storage", "database_url", config.storage_configuration.database_url
        )
        config_writer.set(
            "storage", "file_storage_url", config.storage_configuration.file_storage_url
        )

        scheduler_configuration = config.scheduler_configuration
        config_writer.set("scheduler", "name", scheduler_configuration.name)
        if scheduler_configuration.name == "Deadline":
            config_writer.set(
                "scheduler",
                "deadline_url",
                cast(DeadlineSchedulerConfiguration, scheduler_configuration).url,
            )

        if config.sentry_configuration.url:
            config_writer.add_section("sentry")
            config_writer.set("sentry", "url", config.sentry_configuration.url)

        config_writer.set(
            "session",
            "lifetime",
            humanfriendly.format_timespan(
                config.session_configuration.lifetime.seconds
            ),
        )

        config_writer.set("oidc", "client_id", config.oidc_configuration.client_id)
        config_writer.set(
            "oidc",
            "client_secret",
            config.oidc_configuration.client_secret.get_secret_value(),
        )
        config_writer.set(
            "oidc", "well_known_url", config.oidc_configuration.well_known_url
        )

        config_writer.write(stream)

    def write_file(self, config: AppConfiguration, path: str) -> None:
        with open(path, "w") as f:
            self.write_stream(config, f)
