import configparser
import os

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration


class AppConfigurationReader:
    def read_file(self, path: str) -> AppConfiguration:
        if not os.path.exists(path):
            raise ValueError(f"Supplied config path {path} does not exists!")
        config = configparser.ConfigParser()
        config.read(path)

        storage_configuration = self._read_storage_configuration(config)

        return AppConfiguration(
            port=config.getint("app", "port"),
            debug=config.getboolean("app", "debug", fallback=False),
            storage_configuration=storage_configuration,
        )

    def _read_storage_configuration(
        self, config: configparser.ConfigParser
    ) -> StorageConfiguration:
        return StorageConfiguration(
            database_url=config.get("storage", "database_url"),
            file_storage_url=config.get("storage", "file_storage_url"),
        )
