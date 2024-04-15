import pytest

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_server.api.validators.create_test_edits_validators import (
    CreateComparisonSettingsEditValidator,
    CreateReferenceImageEditValidator,
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
        data = {"testResultId": 1, "newValue": {"method": "SSIM", "threshold": 1}}

        errors = validator.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"testResultId": 1, "newValue": {"method": "SSIM", "threshold": 1}},
                {"id": ["No TestResult with id 1 exists!"]},
            ),
            (
                {"testResultId": 2, "newValue": {"method": "SSIM", "threshold": 1}},
                {
                    "comparisonSettings": [
                        "Can't edit a test result which has no comparison " "settings!"
                    ]
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.side_effect = lambda x: (
            None if x == 1 else test_result_factory()
        )
        validator = CreateComparisonSettingsEditValidator(mock_test_result_repository)

        errors = validator.validate(data)

        assert errors == expected_errors


class TestCreateReferenceImageSettingsEditValidator:
    def test_success(self, test_result_factory):
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.return_value = test_result_factory(
            image_output=5,
            comparison_settings=ComparisonSettings(
                method=ComparisonMethod.SSIM, threshold=1
            ),
        )
        validator = CreateReferenceImageEditValidator(mock_test_result_repository)
        data = {"testResultId": 1}

        errors = validator.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"testResultId": 1},
                {"id": ["No TestResult with id 1 exists!"]},
            ),
            (
                {"testResultId": 2},
                {
                    "testResultId": [
                        "Can't edit a test result which has no image output!"
                    ]
                },
            ),
            (
                {"testResultId": 3},
                {
                    "comparisonSettings": [
                        "Can't edit a test result which has no comparison " "settings!"
                    ]
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors, test_result_factory):
        test_results = {
            1: None,
            2: test_result_factory(
                image_output=None,
                comparison_settings=ComparisonSettings(
                    method=ComparisonMethod.SSIM, threshold=1
                ),
            ),
            3: test_result_factory(image_output=1, comparison_settings=None),
        }
        mock_test_result_repository = mock_safe(TestResultRepository)
        mock_test_result_repository.find_by_id.side_effect = lambda x: test_results[x]
        validator = CreateReferenceImageEditValidator(mock_test_result_repository)

        errors = validator.validate(data)

        assert errors == expected_errors
