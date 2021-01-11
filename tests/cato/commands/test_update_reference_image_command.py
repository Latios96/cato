from cato.commands.update_missing_reference_image import UpdateReferenceImageCommand
from cato.config.config_file_parser import JsonConfigParser
from cato.runners.update_reference_images import UpdateReferenceImage
from cato_server.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe


def test_should_update_correctly(config_fixture):
    mock_json_parser = mock_safe(JsonConfigParser)
    mock_update_reference_image = mock_safe(UpdateReferenceImage)
    update_reference_image_command = UpdateReferenceImageCommand(
        mock_json_parser, mock_update_reference_image
    )
    mock_json_parser.parse.return_value = config_fixture

    update_reference_image_command.update("cato.json", "suite/path")

    mock_json_parser.parse.assert_called_with(
        update_reference_image_command._config_path("cato.json")
    )
    mock_update_reference_image.update.assert_called_with(
        config_fixture, TestIdentifier.from_string("suite/path")
    )