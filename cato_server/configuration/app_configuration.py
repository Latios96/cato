from dataclasses import dataclass

from cato_server.configuration.parts.celery_configuration import CeleryConfiguration
from cato_server.configuration.parts.logging_configuration import LoggingConfiguration
from cato_server.configuration.oidc_config import OidcConfiguration
from cato_server.configuration.parts.oiio_configuration import OiioConfiguration
from cato_server.configuration.parts.scheduler_configuration import (
    SchedulerConfiguration,
)
from cato_server.configuration.parts.secrets_configuration import SecretsConfiguration
from cato_server.configuration.parts.sentry_configuration import SentryConfiguration
from cato_server.configuration.parts.session_configuration import SessionConfiguration
from cato_server.configuration.parts.storage_configuration import StorageConfiguration


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
    oiio_configuration: OiioConfiguration
