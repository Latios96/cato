import datetime

from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_common.domain.test_status import TestStatus
from cato.domain.test_suite import find_test_by_test_identifier
from cato.reporter.reporter import Reporter
from cato.runners.sync_comparison_settings import SyncComparisonSettings
from cato_common.domain.test_edit import (
    ComparisonSettingsEdit,
    ComparisonSettingsEditValue,
)
from cato_common.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe


def test_should_update_successfully(config_fixture):
    mock_config_file_writer = mock_safe(ConfigFileWriter)
    mock_reporter = mock_safe(Reporter)
    sync_comparison_settings = SyncComparisonSettings(
        mock_config_file_writer, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/My_first_test")
    comparison_settings_edits = [create_comparison_settings_edit(test_identifier)]

    sync_comparison_settings.update(
        config_fixture.RUN_CONFIG, "config_file_path", comparison_settings_edits
    )

    mock_config_file_writer.write_to_file.assert_called_with(
        "config_file_path", config_fixture.RUN_CONFIG
    )
    assert find_test_by_test_identifier(
        config_fixture.RUN_CONFIG.suites, test_identifier
    ).comparison_settings == ComparisonSettings(
        method=ComparisonMethod.SSIM, threshold=1
    )
    mock_reporter.report_message.assert_called_with(
        f"Updating My_first_test_Suite/My_first_test to method=SSIM, threshold=1"
    )


def test_no_edits_to_sync_should_not_write(config_fixture):
    mock_config_file_writer = mock_safe(ConfigFileWriter)
    mock_reporter = mock_safe(Reporter)
    sync_comparison_settings = SyncComparisonSettings(
        mock_config_file_writer, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/My_first_test")

    sync_comparison_settings.update(config_fixture.RUN_CONFIG, "config_file_path", [])

    mock_config_file_writer.write_to_file.assert_not_called()
    assert (
        find_test_by_test_identifier(
            config_fixture.RUN_CONFIG.suites, test_identifier
        ).comparison_settings
        == ComparisonSettings.default()
    )


def test_test_for_edit_not_found_in_config_should_print_message_and_not_write(
    config_fixture,
):
    mock_config_file_writer = mock_safe(ConfigFileWriter)
    mock_reporter = mock_safe(Reporter)
    sync_comparison_settings = SyncComparisonSettings(
        mock_config_file_writer, mock_reporter
    )
    test_identifier = TestIdentifier.from_string("My_first_test_Suite/not existing")

    sync_comparison_settings.update(
        config_fixture.RUN_CONFIG,
        "config_file_path",
        [create_comparison_settings_edit(test_identifier)],
    )

    mock_config_file_writer.write_to_file.assert_not_called()
    mock_reporter.report_message.assert_called_with(
        f"No test with identifier {test_identifier} found in config, skipping edit.."
    )
    assert (
        find_test_by_test_identifier(
            config_fixture.RUN_CONFIG.suites,
            TestIdentifier.from_string("My_first_test_Suite/My_first_test"),
        ).comparison_settings
        == ComparisonSettings.default()
    )


def create_comparison_settings_edit(test_identifier):
    return ComparisonSettingsEdit(
        id=0,
        test_id=1,
        test_identifier=test_identifier,
        created_at=datetime.datetime.now(),
        new_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
            status=TestStatus.SUCCESS,
            message=None,
            diff_image_id=2,
            error_value=1,
        ),
        old_value=ComparisonSettingsEditValue(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=0.5
            ),
            status=TestStatus.FAILED,
            message="Failed",
            diff_image_id=2,
            error_value=0.8,
        ),
    )
