import os

from cato.utils.config_utils import resolve_config_path
from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.domain.config import RunConfig


class BaseCliCommand(object):
    def __init__(self, json_config_parser: JsonConfigParser):
        self._json_config_parser = json_config_parser

    def _config_path(self, path: str) -> str:
        return resolve_config_path(path)

    def _read_config(self, config_path: str) -> RunConfig:
        config_path = resolve_config_path(config_path)
        config = self._json_config_parser.parse(config_path)
        # todo add option to pass resources folder as argument
        return RunConfig(
            project_name=config.project_name,
            resource_path=os.path.dirname(config_path),
            suites=config.suites,
            output_folder=os.getcwd(),
            variables=config.variables,
        )
