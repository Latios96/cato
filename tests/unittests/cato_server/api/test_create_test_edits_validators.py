from cato_server.api.validators.create_test_edits_validators import (
    CreateComparisonSettingsEditValidator,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from tests.utils import mock_safe


class TestCreateComparisonSettingsEditValidator:
    def test_success(self, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.return_value = test_result_factory()
        validator = CreateComparisonSettingsEditValidator(mock_test_result_repository)
        data = {"test_result_id": 1, "new_value": {"method": "SSIM", "threshold": 1}}

        errors = validator.validate(data)

        assert errors == {}

    def test_failure(self, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.return_value = None
        validator = CreateComparisonSettingsEditValidator(mock_test_result_repository)
        data = {"test_result_id": 1, "new_value": {"method": "SSIM", "threshold": 1}}

        errors = validator.validate(data)

        assert errors == {"id": ["No TestResult with id 1 exists!"]}
