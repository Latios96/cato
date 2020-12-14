import datetime

import pytest

from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.api.validators.run_validators import CreateRunValidator
from tests.utils import mock_safe


class TestCreateRunValidator:
    def test_success(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateRunValidator(project_repository)

        errors = validator.validate(
            {"project_id": 1, "started_at": str(datetime.datetime.now())}
        )

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"project_id": 2, "started_at": str(datetime.datetime.now())},
                {"project_id": ["No project with id 2 exists!"]},
            ),
            (
                {"project_id": 1, "started_at": "test"},
                {"started_at": ["Not a valid datetime."]},
            ),
        ],
    )
    def testfailure(self, data, expected_errors):
        project_repository = mock_safe(ProjectRepository)
        project_repository.find_by_id = lambda x: x == 1
        validator = CreateRunValidator(project_repository)

        errors = validator.validate(data)

        assert errors == expected_errors
