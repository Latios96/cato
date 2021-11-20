import pytest

from cato_common.domain.result_status import ResultStatus
from cato_server.api.validators.test_result_validators import (
    CreateOutputValidator,
    FinishTestResultValidator,
    StartTestResultValidator,
)
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from tests.utils import mock_safe


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
                "status": ResultStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": 1,
                "reference_image": 2,
                "error_value": 1,
            },
            {
                "id": 1,
                "status": ResultStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": None,
                "error_value": 1,
            },
            {
                "id": 1,
                "status": ResultStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": 1,
                "reference_image": None,
                "error_value": 1,
            },
            {
                "id": 1,
                "status": ResultStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": 2,
                "error_value": 1,
            },
            {
                "id": 1,
                "status": ResultStatus.SUCCESS,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": 2,
                "error_value": None,
            },
            {
                "id": 1,
                "status": ResultStatus.FAILED,
                "message": "test",
                "seconds": 1,
                "image_output": None,
                "reference_image": 2,
                "error_value": None,
                "failure_reason": "TIMED_OUT",
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
                    "status": ResultStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 2,
                    "error_value": None,
                },
                {"id": ["No TestResult with id 42 exists!"]},
            ),
            (
                {
                    "id": 1,
                    "status": ResultStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 42,
                    "reference_image": 2,
                    "error_value": None,
                },
                {"image_output": ["No image exists for id 42."]},
            ),
            (
                {
                    "id": 1,
                    "status": ResultStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 42,
                    "error_value": None,
                },
                {"reference_image": ["No image exists for id 42."]},
            ),
            (
                {
                    "id": 1,
                    "status": ResultStatus.SUCCESS,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 1,
                    "diff_image": 42,
                    "error_value": None,
                },
                {"diff_image": ["No image exists for id 42."]},
            ),
            (
                {
                    "id": 1,
                    "status": ResultStatus.FAILED,
                    "message": "test",
                    "seconds": 1,
                    "image_output": 1,
                    "reference_image": 1,
                    "diff_image": 1,
                    "error_value": None,
                },
                {
                    "failure_reason": [
                        "failure_reason is required is test_status is FAILED"
                    ]
                },
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
