from io import StringIO

from pydantic import SecretStr

from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.configuration.app_configuration_writer import AppConfigurationWriter

EXPECTED = """[app]
port = 5000
debug = False
hostname = localhost
public_url = http://127.0.0.1
workers = 16

[secrets]
sessions_secret = SESSIONS_SECRET
csrf_secret = CSRF_SECRET
api_tokens_secret = API_TOKENS_SECRET

[storage]
database_url = db_url
file_storage_url = file_storage_url

[scheduler]
name = None

[session]
lifetime = 2 hours

[oidc]
client_id = client-id
client_secret = secret
well_known_url = http://somewhere

[celery]
broker_url = pyamqp://guest@localhost//

"""

EXPECTED_SENTRY = """[sentry]
url = the_host
"""


def test_write_stream():
    string_stream = StringIO()
    app_configuration_writer = AppConfigurationWriter()
    config = AppConfigurationDefaults().create()
    config.secrets_configuration.sessions_secret = SecretStr("SESSIONS_SECRET")
    config.secrets_configuration.csrf_secret = SecretStr("CSRF_SECRET")
    config.secrets_configuration.api_tokens_secret = SecretStr("API_TOKENS_SECRET")

    app_configuration_writer.write_stream(config, string_stream)

    assert string_stream.getvalue() == EXPECTED


def test_write_with_sentry():
    string_stream = StringIO()
    app_configuration_writer = AppConfigurationWriter()
    config = AppConfigurationDefaults().create()
    config.sentry_configuration.url = "the_host"

    app_configuration_writer.write_stream(config, string_stream)

    assert EXPECTED_SENTRY in string_stream.getvalue()
