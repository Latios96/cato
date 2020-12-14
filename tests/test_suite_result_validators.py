import pytest

from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_server.api.validators.suite_result_validators import (
    CreateSuiteResultValidator,
)
from tests.utils import mock_safe


class TestCreateSuiteResultValidator:
    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "run_id": ["Missing data for required field."],
                    "suite_name": ["Missing data for required field."],
                    "suite_variables": ["Missing data for required field."],
                },
            ),
            (
                {"run_id": 2},
                {
                    "run_id": ["No run with id 2 exists."],
                    "suite_name": ["Missing data for required field."],
                    "suite_variables": ["Missing data for required field."],
                },
            ),
            (
                {"run_id": 1, "suite_name": "yrsdt*$%$$"},
                {
                    "suite_name": [
                        "invalid char found: invalids=('*'), value='yrsdt*$%$$', reason=INVALID_CHARACTER, target-platform=Windows"
                    ],
                    "suite_variables": ["Missing data for required field."],
                },
            ),
            (
                {
                    "run_id": 1,
                    "suite_name": "suite_name",
                    "suite_variables": {"Test": 6546565},
                },
                {
                    "suite_variables": ["Not a mapping of str->str: Test=6546565"],
                },
            ),
            (
                {
                    "run_id": 1,
                    "suite_name": "existing_suite_name",
                    "suite_variables": {"Test": "test"},
                },
                {
                    "suite_name": [
                        "A test suite with name existing_suite_name already exists for run id 1"
                    ]
                },
            ),
        ],
    )
    def test_invalid_data(self, data, expected_errors):
        run_repo = mock_safe(RunRepository)
        run_repo.find_by_id = lambda x: True if x == 1 else None
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_run_id_and_name = (
            lambda run_id, name: name == "existing_suite_name"
        )
        validator = CreateSuiteResultValidator(run_repo, suite_result_repo)

        errors = validator.validate(data)

        assert errors == expected_errors

    def test_valid_data(self):
        run_repo = mock_safe(RunRepository)
        run_repo.find_by_id.return_value = True
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_run_id_and_name.return_value = False
        validator = CreateSuiteResultValidator(run_repo, suite_result_repo)

        errors = validator.validate(
            {"run_id": 1, "suite_name": "suite_name", "suite_variables": {}}
        )

        assert errors == {}
