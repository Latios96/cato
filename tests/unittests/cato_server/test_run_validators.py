import pytest

from cato_server.api.validators.run_validators import (
    CreateFullRunValidator,
)
from cato_server.storage.abstract.project_repository import ProjectRepository
from tests.utils import mock_safe


class TestCreateFullRunValidator:
    @pytest.mark.parametrize(
        "run_information",
        [
            {
                "os": "WINDOWS",
                "computerName": "cray",
                "localUsername": "username",
                "runInformationType": "LOCAL_COMPUTER",
            },
            {
                "os": "LINUX",
                "computerName": "cray",
                "githubRunId": 3052454707,
                "htmlUrl": "https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
                "jobName": "buildUbuntu",
                "actor": "Latios96",
                "attempt": 1,
                "runNumber": 2,
                "githubUrl": "https://github.com",
                "githubApiUrl": "https://api.github.com",
                "runInformationType": "GITHUB_ACTIONS",
            },
        ],
    )
    def test_success(self, run_information):
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
                "runInformation": run_information,
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
                "runInformation": {
                    "os": "WINDOWS",
                    "computerName": "cray",
                    "localUsername": "username",
                    "runInformationType": "LOCAL_COMPUTER",
                },
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
                "runInformation": {
                    "os": "WINDOWS",
                    "computerName": "cray",
                    "localUsername": "username",
                    "runInformationType": "LOCAL_COMPUTER",
                },
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
                "runInformation": {
                    "os": "WINDOWS",
                    "computerName": "cray",
                    "localUsername": "username",
                    "runInformationType": "LOCAL_COMPUTER",
                },
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
                "runInformation": {
                    "os": "WINDOWS",
                    "computerName": "cray",
                    "localUsername": "username",
                    "runInformationType": "LOCAL_COMPUTER",
                },
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
                "runInformation": {
                    "os": "WINDOWS",
                    "computerName": "cray",
                    "localUsername": "username",
                    "runInformationType": "LOCAL_COMPUTER",
                },
            }
        )

        assert errors == {"branchName": ["Shorter than minimum length 1."]}

    def test_invalid_local_run_information(self):
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
                "runInformation": {
                    "os": "unknown",
                    "computerName": None,
                    "localUsername": None,
                    "runInformationType": "LOCAL_COMPUTER",
                },
            }
        )

        assert errors == {
            "runInformation": {
                "computerName": ["Field may not be null."],
                "localUsername": ["Field may not be null."],
                "os": ["Invalid enum member unknown"],
            }
        }

    def test_invalid_github_actions_run_information(self):
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
                "runInformation": {
                    "os": "LINUX",
                    "computerName": "",
                    "githubRunId": -3052454707,
                    "htmlUrl": "https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
                    "jobName": "buildUbuntu",
                    "actor": "",
                    "attempt": 1,
                    "runNumber": 2,
                    "githubUrl": "https://github.com",
                    "githubApiUrl": "test",
                    "runInformationType": "GITHUB_ACTIONS",
                },
            },
        )

        assert errors == {
            "runInformation": {
                "actor": ["Shorter than minimum length 1."],
                "computerName": ["Shorter than minimum length 1."],
                "githubApiUrl": ["Not a valid URL."],
            }
        }
