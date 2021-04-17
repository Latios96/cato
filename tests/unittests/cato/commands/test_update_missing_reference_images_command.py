import os

from cato.commands.update_reference_image_command import UpdateReferenceImageCommand
from cato.commands.update_missing_reference_images_command import (
    UpdateMissingReferenceImagesCommand,
)
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import RunConfig
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages
from cato.runners.update_reference_images import UpdateReferenceImage
from cato_server.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe


def test_should_update_correctly(config_fixture):
    mock_json_parser = mock_safe(JsonConfigParser)
    mock_update_missing_images = mock_safe(UpdateMissingReferenceImages)
    update_reference_image_command = UpdateMissingReferenceImagesCommand(
        mock_json_parser, mock_update_missing_images
    )
    mock_json_parser.parse.return_value = config_fixture.CONFIG

    update_reference_image_command.update("cato.json")

    mock_json_parser.parse.assert_called_with(
        update_reference_image_command._config_path("cato.json")
    )
    mock_update_missing_images.update.assert_called_with(
        RunConfig(  # todo clean this up
            project_name=config_fixture.CONFIG.project_name,
            path=os.getcwd(),
            test_suites=config_fixture.CONFIG.test_suites,
            output_folder=os.getcwd(),
            variables=config_fixture.CONFIG.variables,
        )
    )
