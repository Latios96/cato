from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
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
        config = self._json_config_parser.parse(path)
        self._update_reference_image.update(
            config, TestIdentifier.from_string(test_identifier)
        )
