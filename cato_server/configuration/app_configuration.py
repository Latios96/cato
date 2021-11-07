from dataclasses import dataclass

from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration


@dataclass
class AppConfiguration:
    port: int
    debug: bool
    storage_configuration: StorageConfiguration
    logging_configuration: LoggingConfiguration
    scheduler_configuration: SchedulerConfiguration
    sentry_configuration: SentryConfiguration
