import binascii
import os

import pytest

from cato.config.config_encoder import ConfigEncoder
from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter


@pytest.fixture
def config_encoder():
    return ConfigEncoder(ConfigFileWriter(), JsonConfigParser())


def test_should_encode_config(config_encoder, config_fixture):
    config_bytes = config_encoder.encode(config_fixture.CONFIG)

    assert (
        config_bytes
        == b"ewogICJwcm9qZWN0X25hbWUiOiAiRVhBTVBMRV9QUk9KRUNUIiwKICAic3VpdGVzIjogWwogICAgewogICAgICAibmFtZSI6ICJNeV9maXJzdF90ZXN0X1N1aXRlIiwKICAgICAgInRlc3RzIjogWwogICAgICAgIHsKICAgICAgICAgICJuYW1lIjogIk15X2ZpcnN0X3Rlc3QiLAogICAgICAgICAgImNvbW1hbmQiOiAibWF5YWJhdGNoIC1zIHtjb25maWdfZmlsZV9mb2xkZXJ9L3t0ZXN0X25hbWUuanNvbn0gLW8ge2ltYWdlX291dHB1dH0ve3Rlc3RfbmFtZS5wbmd9IiwKICAgICAgICAgICJ2YXJpYWJsZXMiOiB7CiAgICAgICAgICAgICJmcmFtZSI6ICI3IgogICAgICAgICAgfQogICAgICAgIH0KICAgICAgXSwKICAgICAgInZhcmlhYmxlcyI6IHsKICAgICAgICAibXlfdmFyIjogImZyb21fc3VpdGUiCiAgICAgIH0KICAgIH0KICBdLAogICJ2YXJpYWJsZXMiOiB7CiAgICAibXlfdmFyIjogImZyb21fY29uZmlnIgogIH0KfQ=="
    )


def test_should_not_decode_not_base64(config_encoder):
    with pytest.raises(binascii.Error):
        config_encoder.decode(b"wurst", "test/path")


def test_should_decode(config_encoder, config_fixture):
    decoded_config = config_encoder.decode(
        b"ewogICJwcm9qZWN0X25hbWUiOiAiRVhBTVBMRV9QUk9KRUNUIiwKICAic3VpdGVzIjogWwogICAgewogICAgICAibmFtZSI6ICJNeV9maXJzdF90ZXN0X1N1aXRlIiwKICAgICAgInRlc3RzIjogWwogICAgICAgIHsKICAgICAgICAgICJuYW1lIjogIk15X2ZpcnN0X3Rlc3QiLAogICAgICAgICAgImNvbW1hbmQiOiAibWF5YWJhdGNoIC1zIHtjb25maWdfZmlsZV9mb2xkZXJ9L3t0ZXN0X25hbWUuanNvbn0gLW8ge2ltYWdlX291dHB1dH0ve3Rlc3RfbmFtZS5wbmd9IiwKICAgICAgICAgICJ2YXJpYWJsZXMiOiB7CiAgICAgICAgICAgICJmcmFtZSI6ICI3IgogICAgICAgICAgfQogICAgICAgIH0KICAgICAgXSwKICAgICAgInZhcmlhYmxlcyI6IHsKICAgICAgICAibXlfdmFyIjogImZyb21fc3VpdGUiCiAgICAgIH0KICAgIH0KICBdLAogICJ2YXJpYWJsZXMiOiB7CiAgICAibXlfdmFyIjogImZyb21fY29uZmlnIgogIH0KfQ==",
        "test/path",
    )

    assert decoded_config.path == "test"
    decoded_config.output_folder = "output"  # todo fix
    assert decoded_config == config_fixture.CONFIG
