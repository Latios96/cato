from cato_server.api.validators.run_validators import (
    CreateFullRunValidator,
)
from cato_server.storage.abstract.project_repository import ProjectRepository
from tests.utils import mock_safe


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
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
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
                                "machine_info": {
                                    "cpu_name": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
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
                                "testd_identifier": "test/identifier",
                                "test_command": "cmd",
                                "test_variables": {},
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
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
                        0: {"test_identifier": ["Missing data for " "required field."]}
                    }
                }
            }
        }

    def test_duplicate_suite_name(self):
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
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    },
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
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    },
                ],
            }
        )

        assert errors == {"test_suites": ["duplicate suite name(s): ['my_suite']"]}

    def test_duplicate_test_name(self):
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
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            },
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
                                "comparison_settings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            },
                        ],
                    },
                ],
            }
        )

        assert errors == {"test_results": ["duplicate test name(s): ['test_name']"]}
