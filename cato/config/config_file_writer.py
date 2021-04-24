import dataclasses
import json
from typing import IO, Dict, cast

import attr

from cato.domain.config import Config
from cato_common.utils.typing import safe_cast


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        if attr.has(o):
            return attr.asdict(o)
        return super().default(o)


class ConfigFileWriter:
    def write_to_file(self, path: str, config: Config) -> None:
        with open(path, "w") as f:
            self.write_to_stream(f, config)

    def write_to_stream(self, stream: IO, config: Config) -> None:
        json.dump(config.for_json(), stream, cls=EnhancedJSONEncoder, indent=2)

    def write_to_dict(self, config: Config) -> Dict:
        json_str = json.dumps(config.for_json(), cls=EnhancedJSONEncoder)
        return safe_cast(dict, json.loads(json_str))
