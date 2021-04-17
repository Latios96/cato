import os

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import RunConfig
from cato.runners.update_reference_images import UpdateReferenceImage
from cato_server.domain.test_identifier import TestIdentifier


class UpdateReferenceImageCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        update_reference_image: UpdateReferenceImage,
    ):
        self._json_config_parser = json_config_parser
        self._update_reference_image = update_reference_image

    def update(self, path, test_identifier: str):
        path = self._config_path(path)
        c = self._json_config_parser.parse(path)  # todo clean this up
        config = RunConfig(
            project_name=c.project_name,
            path=os.path.dirname(path),
            test_suites=c.test_suites,
            output_folder=os.getcwd(),
            variables=c.variables,
        )
        self._update_reference_image.update(
            config, TestIdentifier.from_string(test_identifier)
        )
