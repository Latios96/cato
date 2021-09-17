import pytest

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.api.validators.create_test_edits_validators import (
    CreateComparisonSettingsEditValidator,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from tests.utils import mock_safe


class TestCreateComparisonSettingsEditValidator:
    def test_success(self, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.return_value = test_result_factory(
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
        )
        validator = CreateComparisonSettingsEditValidator(mock_test_result_repository)
        data = {"test_result_id": 1, "new_value": {"method": "SSIM", "threshold": 1}}

        errors = validator.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"test_result_id": 1, "new_value": {"method": "SSIM", "threshold": 1}},
                {"id": ["No TestResult with id 1 exists!"]},
            ),
            (
                {"test_result_id": 2, "new_value": {"method": "SSIM", "threshold": 1}},
                {
                    "comparison_settings": [
                        "Can't edit a test result which has no comparison " "settings!"
                    ]
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.side_effect = (
            lambda x: None if x == 1 else test_result_factory()
        )
        validator = CreateComparisonSettingsEditValidator(mock_test_result_repository)

        errors = validator.validate(data)

        assert errors == expected_errors
