from unittest import mock

from cato.commands.update_reference_image_command import UpdateReferenceImageCommand
from cato_common.config.config_file_parser import JsonConfigParser
from cato.runners.update_reference_images import UpdateReferenceImage
from cato_common.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe

CLI_VARS = {"my_cli_var": "my_cli_value"}


def test_should_update_correctly(config_fixture):
    mock_json_parser = mock_safe(JsonConfigParser)
    mock_update_reference_image = mock_safe(UpdateReferenceImage)
    update_reference_image_command = UpdateReferenceImageCommand(
        mock_json_parser, mock_update_reference_image
    )
    update_reference_image_command._read_config = mock.MagicMock(
        return_value=config_fixture.RUN_CONFIG
    )

    update_reference_image_command.update("cato.json", "suite/path", CLI_VARS)
    mock_update_reference_image.update.assert_called_with(
        config_fixture.RUN_CONFIG,
        TestIdentifier.from_string("suite/path"),
    )
    update_reference_image_command._read_config.assert_called_with(
        "cato.json", CLI_VARS
    )
