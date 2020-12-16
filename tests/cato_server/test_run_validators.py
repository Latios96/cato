import datetime

import pytest

from cato_server.storage.abstract.project_repository import ProjectRepository
from cato_server.api.validators.run_validators import (
    CreateRunValidator,
    CreateFullRunValidator,
)
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


class TestCreateFullRunValidator:
    def test_success(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "project_id": 1,
                "test_suites": [
                    {
                        "suite_name": "my_suite",
                        "suite_variables": {},
                        "tests": [
                            {
                                "test_name": "test_name",
                                "test_identifier": "test/identifier",
                                "test_command": "cmd",
                                "test_variables": {},
                                "execution_status": "NOT_STARTED",
                                "machine_info": {
                                    "cpu_name": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                            }
                        ],
                    }
                ],
            }
        )

        assert errors == {}

    def test_not_existing_project_id(self):
        project_repository = mock_safe(ProjectRepository)
        project_repository.find_by_id.return_value = None
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "project_id": 42,
                "test_suites": [
                    {
                        "suite_name": "my_suite",
                        "suite_variables": {},
                        "tests": [
                            {
                                "test_name": "test_name",
                                "test_identifier": "test/identifier",
                                "test_command": "cmd",
                                "test_variables": {},
                                "execution_status": "NOT_STARTED",
                                "machine_info": {
                                    "cpu_name": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                            }
                        ],
                    }
                ],
            }
        )

        assert errors == {"project_id": ["No project with id 42 exists!"]}

    def test_invalid_nested(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "project_id": 42,
                "test_suites": [
                    {
                        "suite_name": "my_suite",
                        "suite_variables": {},
                        "tests": [
                            {
                                "test_name": "test_name",
                                "test_identifier": "test/identifier",
                                "test_command": "cmd",
                                "test_variables": {},
                                "execution_status": "NOT_SccTARTED",
                                "machine_info": {
                                    "cpu_name": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                            }
                        ],
                    }
                ],
            }
        )

        assert errors == {
            "test_suites": {
                0: {
                    "tests": {
                        0: {"execution_status": ["Invalid enum member NOT_SccTARTED"]}
                    }
                }
            }
        }
