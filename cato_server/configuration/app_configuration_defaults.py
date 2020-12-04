from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration


class AppConfigurationDefault:

    def create(self) -> AppConfiguration:
        return AppConfiguration(
            port=5000,
            debug=False,
            storage_configuration=StorageConfiguration(
                database_url="db_url", file_storage_url="file_storage_url"
            ),
        )
