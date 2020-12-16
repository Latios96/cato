from dataclasses import dataclass

from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.message_queue_configuration import (
    MessageQueueConfiguration,
)
from cato_server.configuration.storage_configuration import StorageConfiguration


@dataclass
class AppConfiguration:
    port: int
    debug: bool
    storage_configuration: StorageConfiguration
    logging_configuration: LoggingConfiguration
    message_queue_configuration: MessageQueueConfiguration
