from dataclasses import dataclass

from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration
from cato_server.domain.auth.secret_str import SecretStr


@dataclass
class AppConfiguration:
    port: int
    debug: bool
    secret: SecretStr
    storage_configuration: StorageConfiguration
    logging_configuration: LoggingConfiguration
    scheduler_configuration: SchedulerConfiguration
    sentry_configuration: SentryConfiguration
    session_configuration: SessionConfiguration
