import json
from typing import IO, Dict

from cato.domain.config import Config
from cato_server.mappers.object_mapper import ObjectMapper


class ConfigFileWriter:
    def __init__(self, object_mapper: ObjectMapper):
        self._object_mapper = object_mapper

    def write_to_file(self, path: str, config: Config) -> None:
        with open(path, "w") as f:
            self.write_to_stream(f, config)

    def write_to_stream(self, stream: IO, config: Config) -> None:
        json.dump(self._object_mapper.to_dict(config), stream, indent=2)

    def write_to_dict(self, config: Config) -> Dict:
        return self._object_mapper.to_dict(config)
