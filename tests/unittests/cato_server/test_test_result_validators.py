import datetime

import pytest

from cato.domain.test_status import TestStatus
from cato_server.storage.abstract.abstract_file_storage import AbstractFileStorage
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.suite_result_repository import SuiteResultRepository
from cato_common.domain.suite_result import SuiteResult
from cato_server.api.validators.test_result_validators import (
    UpdateTestResultValidator,
    CreateOutputValidator,
    FinishTestResultValidator,
    StartTestResultValidator,
)
from tests.utils import mock_safe


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


class TestCreateOutputValidator:
    def test_success(self):
        test_result_repo = mock_safe(TestResultRepository)
        test_result_repo.find_by_id.return_value = True
        output_repository = mock_safe(OutputRepository)
        output_repository.find_by_test_result_id.return_value = None
        validator = CreateOutputValidator(test_result_repo, output_repository)

        errors = validator.validate({"test_result_id": 1, "text": "my text"})

        assert errors == {}

    def test_failure_invalid_test_result_id(self):
        test_result_repo = mock_safe(TestResultRepository)
        test_result_repo.find_by_id.return_value = False
        output_repository = mock_safe(OutputRepository)
        output_repository.find_by_test_result_id.return_value = None
        validator = CreateOutputValidator(test_result_repo, output_repository)

        errors = validator.validate({"test_result_id": 1, "text": "my text"})

        assert errors == {"test_result_id": ["No test result exists for id 1."]}

    def test_failure_existing_output(self):
        test_result_repo = mock_safe(TestResultRepository)
        test_result_repo.find_by_id.return_value = True
        output_repository = mock_safe(OutputRepository)
        output_repository.find_by_test_result_id.return_value = True
        validator = CreateOutputValidator(test_result_repo, output_repository)

        errors = validator.validate({"test_result_id": 1, "text": "my text"})

        assert errors == {
            "test_result_id": ["An output already exists for test result with id 1."]
        }


class TestFinishTestResultValidator:
    @pytest.mark.parametrize(
        "data",
        [
            {
                "id": 1,
                "status": TestStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": 1,
                "reference_image": 2,
            },
            {
                "id": 1,
                "status": TestStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": None,
            },
            {
                "id": 1,
                "status": TestStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": 1,
                "reference_image": None,
            },
            {
                "id": 1,
                "status": TestStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": 2,
            },
        ],
    )
    def test_success(self, data):
        test_result_repository = mock_safe(TestResultRepository)
        image_repository = mock_safe(ImageRepository)
        finish_test_result_validator = FinishTestResultValidator(
            test_result_repository, image_repository
        )

        errors = finish_test_result_validator.validate(data)
        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {
                    "id": 42,
                    "status": TestStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 2,
                },
                {"id": ["No TestResult with id 42 exists!"]},
            ),
            (
                {
                    "id": 1,
                    "status": TestStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 42,
                    "reference_image": 2,
                },
                {"image_output": ["No image exists for id 42."]},
            ),
            (
                {
                    "id": 1,
                    "status": TestStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 42,
                },
                {"reference_image": ["No image exists for id 42."]},
            ),
            (
                {
                    "id": 1,
                    "status": TestStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 1,
                    "diff_image": 42,
                },
                {"diff_image": ["No image exists for id 42."]},
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        test_result_repository = mock_safe(TestResultRepository)
        test_result_repository.find_by_id = lambda x: x == 1
        image_repository = mock_safe(ImageRepository)
        image_repository.find_by_id = lambda x: x in (1, 2)
        finish_test_result_validator = FinishTestResultValidator(
            test_result_repository, image_repository
        )

        errors = finish_test_result_validator.validate(data)
        assert errors == expected_errors


class TestStartTestResultValidator:
    @pytest.mark.parametrize(
        "data",
        [
            {
                "id": 1,
                "machine_info": {
                    "cpu_name": "test",
                    "cores": 8,
                    "memory": 8,
                },
            },
        ],
    )
    def test_success(self, data):
        test_result_repository = mock_safe(TestResultRepository)
        start_test_result_validator = StartTestResultValidator(test_result_repository)

        errors = start_test_result_validator.validate(data)
        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {
                    "id": 42,
                    "machine_info": {
                        "cpu_name": "test",
                        "cores": 8,
                        "memory": 8,
                    },
                },
                {"id": ["No TestResult with id 42 exists!"]},
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        test_result_repository = mock_safe(TestResultRepository)
        test_result_repository.find_by_id = lambda x: x == 1
        start_test_result_validator = StartTestResultValidator(test_result_repository)

        errors = start_test_result_validator.validate(data)
        assert errors == expected_errors
