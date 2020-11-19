import dataclasses
import json
from typing import IO

from cato.domain.config import Config


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


class ConfigFileWriter:
    def write_to_file(self, path: str, config: Config):
        with open(path, "w") as f:
            self.write_to_stream(f, config)

    def write_to_stream(self, stream: IO, config: Config):
        json.dump(config.for_json(), stream, cls=EnhancedJSONEncoder, indent=2)
