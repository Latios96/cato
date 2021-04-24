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
        super(UpdateReferenceImageCommand, self).__init__(json_config_parser)
        self._update_reference_image = update_reference_image

    def update(self, path: str, test_identifier: str) -> None:
        config = self._read_config(path)

        self._update_reference_image.update(
            config, TestIdentifier.from_string(test_identifier)
        )
