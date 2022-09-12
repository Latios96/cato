import mock

from cato.commands.update_missing_reference_images_command import (
    UpdateMissingReferenceImagesCommand,
)
from cato_common.config.config_file_parser import JsonConfigParser
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages
from tests.utils import mock_safe

CLI_VARS = {"my_cli_var": "my_cli_value"}


def test_should_update_correctly(config_fixture):
    mock_json_parser = mock_safe(JsonConfigParser)
    mock_update_missing_images = mock_safe(UpdateMissingReferenceImages)
    update_reference_image_command = UpdateMissingReferenceImagesCommand(
        mock_json_parser, mock_update_missing_images
    )
    update_reference_image_command._read_config = mock.MagicMock(
        return_value=config_fixture.RUN_CONFIG
    )

    update_reference_image_command.update("cato.json", CLI_VARS)

    mock_update_missing_images.update.assert_called_with(config_fixture.RUN_CONFIG)
    update_reference_image_command._read_config.assert_called_with(
        "cato.json", CLI_VARS
    )
