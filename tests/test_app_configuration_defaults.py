from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_defaults import AppConfigurationDefault
from cato_server.configuration.storage_configuration import StorageConfiguration


def test_create_default_config():
    configuration_default = AppConfigurationDefault()

    config = configuration_default.create()

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        storage_configuration=StorageConfiguration(
            database_url="db_url", file_storage_url="file_storage_url"
        ),
    )
