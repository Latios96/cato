from typing import List

from cato_common.config.config_file_writer import ConfigFileWriter
from cato_common.domain.config import RunConfig
from cato_common.domain.test_suite import (
    find_test_by_test_identifier,
)
from cato.reporter.reporter import Reporter
from cato_common.domain.test_edit import ComparisonSettingsEdit


class SyncComparisonSettings:
    def __init__(
        self,
        config_file_writer: ConfigFileWriter,
        reporter: Reporter,
    ):
        self._config_file_writer = config_file_writer
        self._reporter = reporter

    def update(
        self,
        config: RunConfig,
        path: str,
        comparison_settings_edits: List[ComparisonSettingsEdit],
    ) -> None:
        config_was_changed = False
        for edit in comparison_settings_edits:
            had_update = self._update_test(config, edit)
            if had_update:
                config_was_changed = True

        if config_was_changed:
            self._config_file_writer.write_to_file(path, config)

    def _update_test(self, config: RunConfig, edit: ComparisonSettingsEdit) -> bool:
        test = find_test_by_test_identifier(config.suites, edit.test_identifier)
        if not test:
            self._reporter.report_message(
                f"No test with identifier {edit.test_identifier} found in config, skipping edit.."
            )
            return False
        test.comparison_settings = edit.new_value.comparison_settings
        self._reporter.report_message(
            f"Updating {edit.test_identifier} to method={edit.new_value.comparison_settings.method.value}, threshold={edit.new_value.comparison_settings.threshold}"
        )
        return True
