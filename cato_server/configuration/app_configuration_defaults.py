import os

from cato_server.configuration.app_configuration import AppConfiguration
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
from cato_server.domain.auth.secret_str import SecretStr

TEN_MEGABYTES = 10_000_000


class AppConfigurationDefaults:
    DEBUG_DEFAULT = False
    PORT_DEFAULT = 5000
    LOG_FILE_PATH_DEFAULT = "log.txt"
    USE_FILE_HANDLER_DEFAULT = True
    MAX_BYTES_DEFAULT = TEN_MEGABYTES
    BACKUP_COUNT_DEFAULT = 10

    def create(self) -> AppConfiguration:
        return AppConfiguration(
            port=self.PORT_DEFAULT,
            debug=self.DEBUG_DEFAULT,
            secrets_configuration=SecretsConfiguration.default(),
            hostname="localhost",
            public_url="http://127.0.0.1",
            workers=16,
            storage_configuration=StorageConfiguration(
                database_url="db_url", file_storage_url="file_storage_url"
            ),
            logging_configuration=LoggingConfiguration(
                log_file_path=self.LOG_FILE_PATH_DEFAULT,
                use_file_handler=self.USE_FILE_HANDLER_DEFAULT,
                max_bytes=self.MAX_BYTES_DEFAULT,
                backup_count=self.BACKUP_COUNT_DEFAULT,
            ),
            scheduler_configuration=SchedulerConfiguration(),
            sentry_configuration=SentryConfiguration.default(),
            session_configuration=SessionConfiguration.default(),
            oidc_configuration=OidcConfiguration(
                client_id="client-id",
                client_secret=SecretStr("secret"),
                well_known_url="http://somewhere",
            ),
            celery_configuration=CeleryConfiguration(
                broker_url="pyamqp://guest@localhost//"
            ),
            oiio_configuration=OiioConfiguration(thread_count=1),
        )

    def create_ready_to_use(self, config_folder) -> AppConfiguration:
        return AppConfiguration(
            port=self.PORT_DEFAULT,
            debug=self.DEBUG_DEFAULT,
            secrets_configuration=SecretsConfiguration.default(),
            hostname="localhost",
            public_url="http://127.0.0.1",
            workers=16,
            storage_configuration=StorageConfiguration(
                database_url="sqlite:///{}".format(
                    os.path.join(config_folder, "cato.db")
                ),
                file_storage_url=os.path.join(config_folder, "file_storage"),
            ),
            logging_configuration=LoggingConfiguration(
                log_file_path=self.LOG_FILE_PATH_DEFAULT,
                use_file_handler=self.USE_FILE_HANDLER_DEFAULT,
                max_bytes=self.MAX_BYTES_DEFAULT,
                backup_count=self.BACKUP_COUNT_DEFAULT,
            ),
            scheduler_configuration=SchedulerConfiguration(),
            sentry_configuration=SentryConfiguration.default(),
            session_configuration=SessionConfiguration.default(),
            oidc_configuration=OidcConfiguration(
                client_id="client-id",
                client_secret=SecretStr("secret"),
                well_known_url="http://somewhere",
            ),
            celery_configuration=CeleryConfiguration(
                broker_url="pyamqp://guest@localhost//"
            ),
            oiio_configuration=OiioConfiguration(thread_count=1),
        )
