from cato.commands.base_command import BaseCliCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages


class UpdateMissingReferenceImagesCommand(BaseCliCommand):
    def __init__(
        self,
        json_config_parser: JsonConfigParser,
        update_missing_reference_images: UpdateMissingReferenceImages,
    ):
        super(UpdateMissingReferenceImagesCommand, self).__init__(json_config_parser)
        self._update_missing_reference_images = update_missing_reference_images

    def update(self, path: str):
        config = self._read_config(path)
        self._update_missing_reference_images.update(config)
