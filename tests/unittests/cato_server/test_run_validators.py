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
                "projectId": 1,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
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
                "projectId": 42,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    }
                ],
            }
        )

        assert errors == {"projectId": ["No project with id 42 exists!"]}

    def test_invalid_nested(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "projectId": 42,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testdIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "comparisonSettings": {
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
            "testSuites": {
                0: {
                    "tests": {
                        0: {"testIdentifier": ["Missing data for " "required field."]}
                    }
                }
            }
        }

    def test_duplicate_suite_name(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "projectId": 1,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    },
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    },
                ],
            }
        )

        assert errors == {"testSuites": ["duplicate suite name(s): ['my_suite']"]}

    def test_duplicate_test_name(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "projectId": 1,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            },
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            },
                        ],
                    },
                ],
            }
        )

        assert errors == {"testResults": ["duplicate test name(s): ['test_name']"]}

    def test_invalid_branch_name(self):
        project_repository = mock_safe(ProjectRepository)
        validator = CreateFullRunValidator(project_repository)

        errors = validator.validate(
            {
                "projectId": 1,
                "runBatchIdentifier": {
                    "provider": "LOCAL_COMPUTER",
                    "runName": "mac-os",
                    "runIdentifier": "3046812908-1",
                },
                "testSuites": [
                    {
                        "suiteName": "my_suite",
                        "suiteVariables": {},
                        "tests": [
                            {
                                "testName": "test_name",
                                "testIdentifier": "test/identifier",
                                "testCommand": "cmd",
                                "testVariables": {},
                                "machineInfo": {
                                    "cpuName": "test",
                                    "cores": 8,
                                    "memory": 8,
                                },
                                "comparisonSettings": {
                                    "method": "SSIM",
                                    "threshold": 1,
                                },
                            }
                        ],
                    }
                ],
                "branchName": "",
            }
        )

        assert errors == {"branchName": ["Shorter than minimum length 1."]}
