import base64
from io import StringIO

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config


class ConfigEncoder:
    def __init__(
        self, config_file_writer: ConfigFileWriter, json_config_parser: JsonConfigParser
    ):
        self._config_file_writer = config_file_writer
        self._config_file_parser = json_config_parser

    def encode(self, config: Config) -> bytes:
        string_io = StringIO()
        self._config_file_writer.write_to_stream(string_io, config)
        config_str = string_io.getvalue()
        config_base64 = base64.b64encode(config_str.encode())
        return config_base64

    def decode(self, config_bytes: bytes, path: str) -> Config:
        config_str = base64.b64decode(config_bytes).decode()
        string_io = StringIO(config_str)
        return self._config_file_parser.parse(path, string_io)
