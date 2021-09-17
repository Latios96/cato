import datetime

from cato.domain.comparison_settings import ComparisonSettings
from cato_server.domain.test_edit import ComparisonSettingsEdit
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.abstract.test_result_repository import TestResultRepository


class CreateComparisonSettingsEdit:
    def __init__(
        self,
        test_edit_repository: TestEditRepository,
        test_result_repository: TestResultRepository,
    ):
        self._test_edit_repository = test_edit_repository
        self._test_result_repository = test_result_repository

    def create_edit(
        self, test_result_id, comparison_settings: ComparisonSettings
    ) -> ComparisonSettingsEdit:
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"Could not find a test result with id {test_result_id}")

        created_at = self._get_created_at()
        comparison_settings_edit = ComparisonSettingsEdit(
            id=0,
            test_id=test_result.id,
            created_at=created_at,
            old_value=test_result.comparison_settings,
            new_value=comparison_settings,
        )

        saved_edit = self._test_edit_repository.save(
            comparison_settings_edit.to_test_edit()
        )

        return ComparisonSettingsEdit.from_test_edit(saved_edit)

    def _get_created_at(self):
        return datetime.datetime.now()
