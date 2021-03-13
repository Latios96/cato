import configparser
import logging
from typing import IO

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration

logger = logging.getLogger(__name__)


class AppConfigurationWriter:
    def write_stream(self, config: AppConfiguration, stream: IO):
        config_reader = configparser.ConfigParser()
        config_reader.add_section("app")
        config_reader.add_section("storage")
        config_reader.add_section("message_queue")
        config_reader.add_section("scheduler")
        config_reader.set("app", "port", str(config.port))
        config_reader.set("app", "debug", str(config.debug))
        config_reader.set(
            "storage", "database_url", config.storage_configuration.database_url
        )
        config_reader.set(
            "storage", "file_storage_url", config.storage_configuration.file_storage_url
        )
        config_reader.set(
            "message_queue", "host", config.message_queue_configuration.host
        )

        scheduler_configuration = config.scheduler_configuration
        config_reader.set("scheduler", "name", scheduler_configuration.name)
        if scheduler_configuration.name == "Deadline":
            config_reader.set("scheduler", "deadline_url", scheduler_configuration.url)

        config_reader.write(stream)

    def write_file(self, config: AppConfiguration, path: str):
        with open(path, "w") as f:
            self.write_stream(config, f)
