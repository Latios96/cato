from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
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
        config = self._json_config_parser.parse(path)
        self._update_missing_reference_images.update(config)
