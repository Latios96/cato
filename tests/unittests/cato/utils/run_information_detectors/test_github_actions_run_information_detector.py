import json
from unittest import mock

import pytest
import requests

from cato.utils.run_information_detectors.github_actions_run_information_detector import (
    GithubActionsRunInformationDetector,
)
from cato_common.domain.run_information import OS
from cato_common.dtos.create_full_run_dto import (
    GithubActionsRunInformationForRunCreation,
)


class TestCanDetect:
    def test_can_detect(self):
        env = {"GITHUB_ACTIONS": "true"}
        detector = GithubActionsRunInformationDetector(environment=env)

        assert detector.can_detect()

    def test_can_not_detect(self):
        env = {}
        detector = GithubActionsRunInformationDetector(environment=env)

        assert not detector.can_detect()


class TestDetect:

    RESPONSE = {
        "jobs": [
            {
                "check_run_url": "https://api.github.com/repos/owner/repo-name/check-runs/8349218719",
                "completed_at": "2022-09-14T11:34:33Z",
                "conclusion": "success",
                "head_sha": "1eff2ef8f0c8aa282a6014f8a120fcf1dc641b03",
                "html_url": "https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
                "id": 8349218719,
                "labels": ["ubuntu-latest"],
                "name": "build_ubuntu (3.7)",
                "run_attempt": 1,
                "run_id": 3052454707,
                "run_url": "https://api.github.com/repos/owner/repo-name/actions/runs/3052454707",
                "runner_group_id": 2,
                "runner_group_name": "GitHub Actions",
                "runner_id": 1,
                "runner_name": "Hosted Agent",
                "started_at": "2022-09-14T11:34:24Z",
                "status": "completed",
                "steps": [
                    {
                        "completed_at": "2022-09-14T13:34:27.000+02:00",
                        "conclusion": "success",
                        "name": "Set up job",
                        "number": 1,
                        "started_at": "2022-09-14T13:34:24.000+02:00",
                        "status": "completed",
                    },
                    {
                        "completed_at": "2022-09-14T13:34:30.000+02:00",
                        "conclusion": "success",
                        "name": "Run actions/checkout@v1",
                        "number": 2,
                        "started_at": "2022-09-14T13:34:27.000+02:00",
                        "status": "completed",
                    },
                    {
                        "completed_at": "2022-09-14T13:34:30.000+02:00",
                        "conclusion": "success",
                        "name": "Set up Python 3.7",
                        "number": 3,
                        "started_at": "2022-09-14T13:34:30.000+02:00",
                        "status": "completed",
                    },
                    {
                        "completed_at": "2022-09-14T13:34:31.000+02:00",
                        "conclusion": "success",
                        "name": "Dump env",
                        "number": 4,
                        "started_at": "2022-09-14T13:34:31.000+02:00",
                        "status": "completed",
                    },
                    {
                        "completed_at": "2022-09-14T13:34:33.000+02:00",
                        "conclusion": "success",
                        "name": "Upload env",
                        "number": 5,
                        "started_at": "2022-09-14T13:34:33.000+02:00",
                        "status": "completed",
                    },
                    {
                        "completed_at": "2022-09-14T13:34:31.000+02:00",
                        "conclusion": "success",
                        "name": "Complete job",
                        "number": 6,
                        "started_at": "2022-09-14T13:34:31.000+02:00",
                        "status": "completed",
                    },
                ],
                "url": "https://api.github.com/repos/owner/repo-name/actions/jobs/8349218719",
            }
        ],
        "total_count": 1,
    }

    @mock.patch("requests.get")
    @mock.patch("cato_common.domain.run_information.OS.get_current_os")
    @mock.patch("socket.gethostname")
    def test_detect_successfully(
        self,
        mock_gethostname,
        mock_get_current_os,
        mock_requests_get,
        github_actions_run_information,
    ):
        mock_get_current_os.return_value = OS.WINDOWS
        mock_gethostname.return_value = "cray"
        response = requests.Response()
        response._content = json.dumps(TestDetect.RESPONSE).encode("utf-8")
        response.status_code = 200
        mock_requests_get.return_value = response
        env = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_RUN_ID": "3052454707",
            "GITHUB_JOB": "build_ubuntu",
            "GITHUB_ACTOR": "owner",
            "GITHUB_RUN_ATTEMPT": "1",
            "GITHUB_RUN_NUMBER": "2",
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_API_URL": "https://api.github.com",
            "GITHUB_REPOSITORY": "owner/repo-name",
            "GITHUB_TOKEN": "the-token",
        }
        detector = GithubActionsRunInformationDetector(environment=env)

        data = detector.detect()

        assert data == GithubActionsRunInformationForRunCreation(
            os=OS.WINDOWS,
            computer_name="cray",
            github_run_id=3052454707,
            html_url="https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
            job_name="build_ubuntu",
            actor="owner",
            attempt=1,
            run_number=2,
            github_url="https://github.com",
            github_api_url="https://api.github.com",
        )

    @mock.patch("requests.get")
    @mock.patch("cato_common.domain.run_information.OS.get_current_os")
    @mock.patch("socket.gethostname")
    def test_detect_successfully(
        self,
        mock_gethostname,
        mock_get_current_os,
        mock_requests_get,
        github_actions_run_information,
    ):
        mock_get_current_os.return_value = OS.WINDOWS
        mock_gethostname.return_value = "cray"
        response = requests.Response()
        response._content = "not found".encode("utf-8")
        response.status_code = 404
        mock_requests_get.return_value = response
        env = {
            "GITHUB_ACTIONS": "true",
            "GITHUB_RUN_ID": "3052454707",
            "GITHUB_JOB": "build_ubuntu",
            "GITHUB_ACTOR": "owner",
            "GITHUB_RUN_ATTEMPT": "1",
            "GITHUB_RUN_NUMBER": "2",
            "GITHUB_SERVER_URL": "https://github.com",
            "GITHUB_API_URL": "https://api.github.com",
            "GITHUB_REPOSITORY": "owner/repo-name",
            "GITHUB_TOKEN": "the-token",
        }
        detector = GithubActionsRunInformationDetector(environment=env)

        with pytest.raises(RuntimeError):
            detector.detect()
