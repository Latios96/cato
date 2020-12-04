from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.storage_configuration import StorageConfiguration




class AppConfigurationDefaults:
    DEBUG_DEFAULT = False
    PORT_DEFAULT = 5000
    def create(self) -> AppConfiguration:
        return AppConfiguration(
            port=self.PORT_DEFAULT,
            debug=self.DEBUG_DEFAULT,
            storage_configuration=StorageConfiguration(
                database_url="db_url", file_storage_url="file_storage_url"
            ),
        )
