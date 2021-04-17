from unittest import mock

from cato.domain.config import Config, RunConfig
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.runners.update_reference_images import UpdateReferenceImage
from cato_server.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example project"
EXISTS_PNG = "exists.png"


def test_should_update():
    mock_copy = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.return_value = EXISTS_PNG
    missing_reference_images = UpdateReferenceImage(output_folder, copy_file=mock_copy)
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        test_suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config, TestIdentifier("example", "my_first_test"))

    mock_copy.assert_called_once_with(
        EXISTS_PNG, "/example/my_first_test/reference.png"
    )


def test_should_not_update_because_image_output_missing():
    mock_copy = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.return_value = None
    missing_reference_images = UpdateReferenceImage(output_folder, copy_file=mock_copy)
    test = Test(name="my_first_test", command="dummy_command", variables={})
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        test_suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config, TestIdentifier("example", "my_first_test"))

    mock_copy.assert_not_called()


def test_user_supplied_paths_are_checked():
    mock_copy = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.side_effect = [EXISTS_PNG, "reference.png"]
    missing_reference_images = UpdateReferenceImage(output_folder, copy_file=mock_copy)
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={
            "image_output": "user_supplied_image_output.png",
            "reference_image": "user_supplied_reference_image.png",
        },
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        test_suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config, TestIdentifier("example", "my_first_test"))

    output_folder.any_existing.assert_called_with(
        [
            "output/result/example/my_first_test/my_first_test.exr",
            "output/result/example/my_first_test/my_first_test.png",
            "user_supplied_image_output.png",
        ]
    )
