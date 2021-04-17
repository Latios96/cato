import os

from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import RunConfig


class BaseCliCommand(object):
    def __init__(self, json_config_parser: JsonConfigParser):
        self._json_config_parser = json_config_parser

    def _config_path(self, path: str) -> str:
        if not path:
            path = os.getcwd()
        path = os.path.abspath(path)
        if os.path.isdir(path):
            path = os.path.join(path, "cato.json")
        return path

    def _read_config(self, config_path: str) -> RunConfig:
        config = self._json_config_parser.parse(config_path)
        # todo add option to pass resources folder as argument
        return RunConfig(
            project_name=config.project_name,
            path=os.path.dirname(config_path),
            test_suites=config.test_suites,
            output_folder=os.getcwd(),
            variables=config.variables,
        )
