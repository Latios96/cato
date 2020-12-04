import os
from io import StringIO

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.app_configuration_writer import AppConfigurationWriter

EXPECTED = """[app]
port = 5000
debug = False

[storage]
database_url = db_url
file_storage_url = file_storage_url

"""


def test_write_stream():
    string_stream = StringIO()
    app_configuration_writer = AppConfigurationWriter()
    config = AppConfigurationDefaults().create()

    app_configuration_writer.write_stream(config, string_stream)

    assert string_stream.getvalue() == EXPECTED
