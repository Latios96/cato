from dataclasses import dataclass

from cato_server.configuration.celery_configuration import CeleryConfiguration
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.scheduler_configuration import SchedulerConfiguration
from cato_server.configuration.secrets_configuration import SecretsConfiguration
from cato_server.configuration.sentry_configuration import SentryConfiguration
from cato_server.configuration.session_configuration import SessionConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration


@dataclass
class AppConfiguration:
    port: int
    debug: bool
    secrets_configuration: SecretsConfiguration
    hostname: str
    public_url: str
    storage_configuration: StorageConfiguration
    logging_configuration: LoggingConfiguration
    scheduler_configuration: SchedulerConfiguration
    sentry_configuration: SentryConfiguration
    session_configuration: SessionConfiguration
    oidc_configuration: OidcConfiguration
    celery_configuration: CeleryConfiguration
