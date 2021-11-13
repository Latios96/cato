import datetime

import pytest

from cato_common.domain.test_status import TestStatus
from cato.reporter.reporter import Reporter
from cato.runners.sync_reference_image_edits import SyncReferenceImageEdits
from cato.variable_processing.variable_processor import VariableProcessor
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.image import Image
from cato_common.domain.test_edit import ReferenceImageEdit, ReferenceImageEditValue
from cato_common.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe


def test_success(tmp_path, config_fixture):
    mock_variable_processor = mock_safe(VariableProcessor)
    mock_variable_processor.evaluate_variables.return_value = {
        "reference_image_png": str(tmp_path / "image.png"),
        "reference_image_exr": str(tmp_path / "image.exr"),
        "reference_image_no_extension": str(tmp_path / "image"),
    }
    mock_cato_api_client = mock_safe(CatoApiClient)
    image = create_image("test.exr")
    mock_cato_api_client.get_image_by_id.return_value = image
    mock_cato_api_client.download_original_image.return_value = b"test exr content"
    mock_reporter = mock_safe(Reporter)
    sync_reference_image_edits = SyncReferenceImageEdits(
        mock_cato_api_client, mock_variable_processor, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/My_first_test")
    reference_image_edit = create_reference_image_edit(test_identifier)

    sync_reference_image_edits.update(config_fixture.RUN_CONFIG, [reference_image_edit])

    assert (tmp_path / "image.exr").exists()
    assert (tmp_path / "image.exr").open().readlines() == ["test exr content"]
    mock_cato_api_client.get_image_by_id.assert_called_with(1)
    mock_cato_api_client.download_original_image.assert_called_with(1)
    mock_variable_processor.evaluate_variables.assert_called_with(
        config_fixture.RUN_CONFIG, config_fixture.TEST_SUITE, config_fixture.TEST
    )
    mock_reporter.report_message.assert_called_with(
        f"Updating My_first_test_Suite/My_first_test to a new reference image at {str(tmp_path / 'image.exr')}"
    )


def test_success_override_file(tmp_path, config_fixture):
    mock_variable_processor = mock_safe(VariableProcessor)
    mock_variable_processor.evaluate_variables.return_value = {
        "reference_image_png": str(tmp_path / "image.png"),
        "reference_image_exr": str(tmp_path / "image.exr"),
        "reference_image_no_extension": str(tmp_path / "image"),
    }
    with (tmp_path / "image.exr").open("w") as f:
        f.write("previos content")
    mock_cato_api_client = mock_safe(CatoApiClient)
    image = create_image("test.exr")
    mock_cato_api_client.get_image_by_id.return_value = image
    mock_cato_api_client.download_original_image.return_value = b"test exr content"
    mock_reporter = mock_safe(Reporter)
    sync_reference_image_edits = SyncReferenceImageEdits(
        mock_cato_api_client, mock_variable_processor, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/My_first_test")
    reference_image_edit = create_reference_image_edit(test_identifier)

    sync_reference_image_edits.update(config_fixture.RUN_CONFIG, [reference_image_edit])

    assert (tmp_path / "image.exr").exists()
    assert (tmp_path / "image.exr").open().readlines() == ["test exr content"]


def test_no_test_found_in_config_should_not_download(tmp_path, config_fixture):
    mock_variable_processor = mock_safe(VariableProcessor)
    mock_variable_processor.evaluate_variables.return_value = {
        "reference_image_png": str(tmp_path / "image.png"),
        "reference_image_exr": str(tmp_path / "image.exr"),
        "reference_image_no_extension": str(tmp_path / "image"),
    }
    mock_cato_api_client = mock_safe(CatoApiClient)
    mock_reporter = mock_safe(Reporter)
    sync_reference_image_edits = SyncReferenceImageEdits(
        mock_cato_api_client, mock_variable_processor, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/not_found")
    reference_image_edit = create_reference_image_edit(test_identifier)

    sync_reference_image_edits.update(config_fixture.RUN_CONFIG, [reference_image_edit])

    mock_cato_api_client.get_image_by_id.assert_not_called()
    mock_cato_api_client.download_original_image.assert_not_called()
    mock_reporter.report_message.assert_called_with(
        f"No test with identifier My_first_test_Suite/not_found found in config, skipping edit.."
    )


def test_no_image_could_be_downloaded(tmp_path, config_fixture):
    mock_variable_processor = mock_safe(VariableProcessor)
    mock_variable_processor.evaluate_variables.return_value = {
        "reference_image_png": str(tmp_path / "image.png"),
        "reference_image_exr": str(tmp_path / "image.exr"),
        "reference_image_no_extension": str(tmp_path / "image"),
    }
    mock_cato_api_client = mock_safe(CatoApiClient)
    image = create_image("test.exr")
    mock_cato_api_client.get_image_by_id.return_value = image
    mock_cato_api_client.download_original_image.return_value = None
    mock_reporter = mock_safe(Reporter)
    sync_reference_image_edits = SyncReferenceImageEdits(
        mock_cato_api_client, mock_variable_processor, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/My_first_test")
    reference_image_edit = create_reference_image_edit(test_identifier)

    sync_reference_image_edits.update(config_fixture.RUN_CONFIG, [reference_image_edit])

    mock_cato_api_client.get_image_by_id.assert_called_with(1)
    mock_cato_api_client.download_original_image.assert_called_with(1)
    mock_reporter.report_message.assert_called_with(
        f"No new reference image found for {test_identifier}, skipping edit.."
    )


@pytest.mark.parametrize(
    "extension,expected_path",
    [
        (".png", "/some/path/image.png"),
        (".exr", "/some/path/image.exr"),
        (".tif", "/some/path/image.tif"),
    ],
)
def test_get_image_path(config_fixture, extension, expected_path):
    mock_variable_processor = mock_safe(VariableProcessor)
    mock_variable_processor.evaluate_variables.return_value = {
        "reference_image_png": "/some/path/image.png",
        "reference_image_exr": "/some/path/image.exr",
        "reference_image_no_extension": "/some/path/image",
    }
    mock_cato_api_client = mock_safe(CatoApiClient)
    mock_reporter = mock_safe(Reporter)
    sync_reference_image_edits = SyncReferenceImageEdits(
        mock_cato_api_client, mock_variable_processor, mock_reporter
    )

    image_path = sync_reference_image_edits._get_image_path(
        config_fixture.RUN_CONFIG,
        config_fixture.TEST_SUITE,
        config_fixture.TEST,
        create_image("test" + extension),
    )

    assert image_path == expected_path


def create_image(name):
    return Image(
        id=0,
        name=name,
        original_file_id=10,
        channels=[],
        width=1920,
        height=1080,
    )


def create_reference_image_edit(test_identifier):
    return ReferenceImageEdit(
        id=0,
        test_id=1,
        test_identifier=test_identifier,
        created_at=datetime.datetime.now(),
        new_value=ReferenceImageEditValue(
            status=TestStatus.SUCCESS,
            message=None,
            reference_image_id=1,
            diff_image_id=2,
            error_value=1,
        ),
        old_value=ReferenceImageEditValue(
            status=TestStatus.FAILED,
            message="Failed",
            reference_image_id=3,
            diff_image_id=4,
            error_value=0.5,
        ),
    )
