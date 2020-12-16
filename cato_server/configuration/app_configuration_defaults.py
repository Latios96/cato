from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.logging_configuration import LoggingConfiguration
from cato_server.configuration.message_queue_configuration import (
    MessageQueueConfiguration,
)
from cato_server.configuration.storage_configuration import StorageConfiguration

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
            storage_configuration=StorageConfiguration(
                database_url="db_url", file_storage_url="file_storage_url"
            ),
            logging_configuration=LoggingConfiguration(
                log_file_path=self.LOG_FILE_PATH_DEFAULT,
                use_file_handler=self.USE_FILE_HANDLER_DEFAULT,
                max_bytes=self.MAX_BYTES_DEFAULT,
                backup_count=self.BACKUP_COUNT_DEFAULT,
            ),
            message_queue_configuration=MessageQueueConfiguration(host="localhost"),
        )
