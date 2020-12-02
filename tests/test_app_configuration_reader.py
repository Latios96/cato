import configparser
import os

import pytest

from cato_server.configuration.app_configuration import AppConfiguration
from cato_server.configuration.app_configuration_reader import AppConfigurationReader
from cato_server.configuration.storage_configuration import StorageConfiguration

VALID_INI_FILE = """[app]
port=5000
debug=True
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url"""

MISSING_PORT = """[app]
[storage]
debug=True
database_url=my_database_url
file_storage_url=my_file_storage_url"""

MISSING_DATABASE_URL = """[app]
port=5000
debug=True
[storage]
file_storage_url=my_file_storage_url"""

MISSING_FILE_STORAGE_URL = """[app]
port=5000
debug=True
[storage]
database_url=my_database_url"""

MISSING_DEBUG = """[app]
port=5000
[storage]
database_url=my_database_url
file_storage_url=my_file_storage_url"""


@pytest.fixture
def ini_file_creator(tmp_path):
    def create_ini_file(content):
        ini_path = os.path.join(str(tmp_path), "config.ini")
        with open(ini_path, "w") as f:
            f.write(content)
        return ini_path

    return create_ini_file


def test_read_not_existing_ini_file():
    reader = AppConfigurationReader()
    with pytest.raises(ValueError):
        reader.read_file("ini_path")


def test_read_valid_file(ini_file_creator):
    ini_path = ini_file_creator(VALID_INI_FILE)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=True,
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
    )


@pytest.mark.parametrize(
    "invalid_config", [MISSING_PORT, MISSING_DATABASE_URL, MISSING_FILE_STORAGE_URL]
)
def test_read_missing_should_fail(invalid_config, ini_file_creator):
    ini_path = ini_file_creator(invalid_config)
    reader = AppConfigurationReader()

    with pytest.raises(configparser.NoOptionError):
        reader.read_file(ini_path)


def test_read_missing_debug_should_default_to_false(ini_file_creator):
    ini_path = ini_file_creator(MISSING_DEBUG)
    reader = AppConfigurationReader()

    config = reader.read_file(ini_path)

    assert config == AppConfiguration(
        port=5000,
        debug=False,
        storage_configuration=StorageConfiguration(
            database_url="my_database_url", file_storage_url="my_file_storage_url"
        ),
    )
