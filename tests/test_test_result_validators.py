import datetime

import pytest

from cato.domain.test_status import TestStatus
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato.domain.suite_result import SuiteResult
from cato_server.api.validators.test_result_validators import (
    CreateTestResultValidator,
    UpdateTestResultValidator,
)
from tests.utils import mock_safe


class TestCreateTestResultValidator:
    def test_success(self):
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_id.return_value = SuiteResult(
            id=1, run_id=1, suite_name="my_suite", suite_variables={}
        )
        file_storage = mock_safe(AbstractFileStorage)
        file_storage.find_by_id = lambda x: x in [1, 2]
        validator = CreateTestResultValidator(suite_result_repo, file_storage)

        errors = validator.validate(
            {
                "suite_result_id": 1,
                "test_name": "my_test_name",
                "test_identifier": "my_suite/my_test_name",
                "test_command": "my_command",
                "test_variables": {"key": "value"},
                "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                "execution_status": "NOT_STARTED",
                "image_output": 1,
                "reference_image": 2,
            }
        )

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {
                    "suite_result_id": 5,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/my_test_name",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "image_output": 1,
                    "reference_image": 2,
                },
                {"suite_result_id": ["No suite result exists for id 5."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "foo/my_test_name",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "image_output": 1,
                    "reference_image": 2,
                },
                {
                    "test_identifier": [
                        "Provided foo/my_test_name does not match suite name my_suite of linked suite result and test name my_test_name"
                    ]
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/bar",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "image_output": 1,
                    "reference_image": 2,
                },
                {
                    "test_identifier": [
                        "Provided my_suite/bar does not match suite name my_suite of linked suite result and test name my_test_name"
                    ]
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/my_test_name",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "image_output": 4,
                    "reference_image": 5,
                },
                {
                    "image_output": ["No file exists for id 4."],
                    "reference_image": ["No file exists for id 5."],
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_id = (
            lambda x: SuiteResult(
                id=1, run_id=1, suite_name="my_suite", suite_variables={}
            )
            if x == 1
            else None
        )
        file_storage = mock_safe(AbstractFileStorage)
        file_storage.find_by_id = lambda x: x in [1, 2]
        validator = CreateTestResultValidator(suite_result_repo, file_storage)

        errors = validator.validate(data)

        assert errors == expected_errors


class TestUpdateTestResultValidator:
    def test_success(self):
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_id.return_value = SuiteResult(
            id=1, run_id=1, suite_name="my_suite", suite_variables={}
        )
        file_storage = mock_safe(AbstractFileStorage)
        file_storage.find_by_id = lambda x: x in [1, 2]
        validator = UpdateTestResultValidator(suite_result_repo, file_storage)

        errors = validator.validate(
            {
                "status": TestStatus.SUCCESS,
                "output": ["1", "2", "3"],
                "seconds": 5,
                "message": "my_message",
                "image_output": 1,
                "reference_image": 1,
                "started_at": datetime.datetime.now().isoformat(),
                "finished_at": datetime.datetime.now().isoformat(),
            }
        )

        assert errors == {}

    def test_failure(self):
        suite_result_repo = mock_safe(SuiteResultRepository)
        suite_result_repo.find_by_id.return_value = SuiteResult(
            id=1, run_id=1, suite_name="my_suite", suite_variables={}
        )
        file_storage = mock_safe(AbstractFileStorage)
        file_storage.find_by_id = lambda x: x in [1, 2]
        validator = UpdateTestResultValidator(suite_result_repo, file_storage)

        errors = validator.validate(
            {
                "status": TestStatus.SUCCESS,
                "output": ["1", "2", "3"],
                "seconds": 5,
                "message": "my_message",
                "image_output": 1,
                "reference_image": 3,
                "started_at": datetime.datetime.now().isoformat(),
                "finished_at": datetime.datetime.now().isoformat(),
            }
        )

        assert errors == {"reference_image": ["No file exists for id 3."]}
