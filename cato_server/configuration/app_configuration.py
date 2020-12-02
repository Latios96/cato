from dataclasses import dataclass

from cato_server.configuration.storage_configuration import StorageConfiguration


@dataclass
class AppConfiguration:
    port: int
    storage_configuration: StorageConfiguration
