import pytest
import requests

from cato_server.schedulers.deadline.deadline_api import DeadlineApi, DeadlineApiError
from cato_server.schedulers.deadline.deadline_job import DeadlineJob
from tests.utils import mock_safe


def create_response(status_code=200):
    response = requests.Response()
    response.status_code = status_code
    return response


class TestDeadlineApi:
    def setup_method(self, method):
        self.http_mock = mock_safe(requests)
        self.deadline_api = DeadlineApi("some_url", http_module=self.http_mock)

    def test_should_submit_jobs_with_success(self):
        jobs = [
            DeadlineJob(job_info={"Plugin": "test"}, plugin_info={"my_value": "test"})
        ]
        self.http_mock.post.return_value = create_response(status_code=200)

        self.deadline_api.submit_jobs(jobs)

        self.http_mock.post.assert_called_once_with(
            "some_url/api/jobs",
            json={
                "Jobs": [
                    {
                        "JobInfo": {"Plugin": "test"},
                        "PluginInfo": {"my_value": "test"},
                        "AuxFiles": [],
                    }
                ]
            },
        )

    def test_should_submit_jobs_with_error_should_throw_error(self):
        jobs = [
            DeadlineJob(job_info={"Plugin": "test"}, plugin_info={"my_value": "test"})
        ]
        self.http_mock.post.return_value = create_response(status_code=500)

        with pytest.raises(DeadlineApiError):
            self.deadline_api.submit_jobs(jobs)

        self.http_mock.post.assert_called_once_with(
            "some_url/api/jobs",
            json={
                "Jobs": [
                    {
                        "JobInfo": {"Plugin": "test"},
                        "PluginInfo": {"my_value": "test"},
                        "AuxFiles": [],
                    }
                ]
            },
        )

    def test_can_not_submit_empty_job_list(self):
        jobs = []

        with pytest.raises(DeadlineApiError):
            self.deadline_api.submit_jobs(jobs)

        self.http_mock.post.assert_not_called()
