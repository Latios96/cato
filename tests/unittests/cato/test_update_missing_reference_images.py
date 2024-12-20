from unittest import mock
from unittest.mock import call

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.runners.update_missing_reference_images import UpdateMissingReferenceImages
from tests.utils import mock_safe

EXAMPLE_PROJECT = "Example project"

EXISTS_PNG = "exists.png"


def test_should_update_missing():
    mock_copy = mock.MagicMock()
    mock_ensure_folder = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.side_effect = [EXISTS_PNG, None]
    missing_reference_images = UpdateMissingReferenceImages(
        output_folder, copy_file=mock_copy, ensure_folder=mock_ensure_folder
    )
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config)

    mock_copy.assert_called_once_with(
        EXISTS_PNG, "/example/my_first_test/reference.png"
    )
    mock_ensure_folder.assert_called_with("/example/my_first_test")


def test_should_not_update_because_exists():
    mock_copy = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.side_effect = [EXISTS_PNG, "reference.png"]
    missing_reference_images = UpdateMissingReferenceImages(
        output_folder, copy_file=mock_copy
    )
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config)

    mock_copy.assert_not_called()


def test_user_supplied_paths_are_checked():
    mock_copy = mock.MagicMock()
    output_folder = mock_safe(OutputFolder)
    output_folder.any_existing.side_effect = [EXISTS_PNG, "reference.png"]
    missing_reference_images = UpdateMissingReferenceImages(
        output_folder, copy_file=mock_copy
    )
    test = Test(
        name="my_first_test",
        command="dummy_command",
        variables={
            "image_output": "user_supplied_image_output.png",
            "reference_image": "user_supplied_reference_image.png",
        },
        comparison_settings=ComparisonSettings.default(),
    )
    test_suite = TestSuite(name="example", tests=[test])
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="",
        suites=[test_suite],
        output_folder="output",
    )

    missing_reference_images.update(config)

    output_folder.any_existing.assert_has_calls(
        [
            call(
                [
                    "output/result/example/my_first_test/my_first_test.exr",
                    "output/result/example/my_first_test/my_first_test.png",
                    "user_supplied_image_output.png",
                ]
            ),
            call(
                [
                    "/example/my_first_test/reference.exr",
                    "/example/my_first_test/reference.png",
                    "user_supplied_reference_image.png",
                ]
            ),
        ]
    )
