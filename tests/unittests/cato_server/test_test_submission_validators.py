from cato_server.api.validators.test_submission_validators import (
    SubmissionInfoValidator,
)
from cato_server.storage.abstract.run_repository import RunRepository
from tests.unittests.cato_common.config.test_config_file_parser import VALID_CONFIG
from tests.utils import mock_safe


def test_success():
    mock_run_repository = mock_safe(RunRepository)
    validator = SubmissionInfoValidator(mock_run_repository)
    mock_run_repository.find_by_id.return_value = True

    errors = validator.validate(
        {
            "config": VALID_CONFIG,
            "runId": 2,
            "resourcePath": "some/path",
            "executable": "some/path",
        }
    )

    assert not errors


def test_not_existing_run_id_should_fail():
    mock_run_repository = mock_safe(RunRepository)
    validator = SubmissionInfoValidator(mock_run_repository)
    mock_run_repository.find_by_id.return_value = False

    errors = validator.validate(
        {
            "config": VALID_CONFIG,
            "runId": 2,
            "resourcePath": "some/path",
            "executable": "some/path",
        }
    )

    assert errors == {"runId": ["No run exists for id 2."]}
