import os

from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import RunConfig
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages


class UpdateMissingReferenceImagesCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        update_missing_reference_images: UpdateMissingReferenceImages,
    ):
        self._json_config_parser = json_config_parser
        self._update_missing_reference_images = update_missing_reference_images

    def update(self, path):
        path = self._config_path(path)
        c = self._json_config_parser.parse(path)
        config = RunConfig(  # todo clean this up
            project_name=c.project_name,
            path=os.path.dirname(path),
            test_suites=c.test_suites,
            output_folder=os.getcwd(),
            variables=c.variables,
        )
        self._update_missing_reference_images.update(config)
