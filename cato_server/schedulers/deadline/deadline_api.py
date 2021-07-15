import logging
from typing import List

import requests

from cato_server.schedulers.deadline.deadline_job import DeadlineJob

logger = logging.getLogger(__name__)


class DeadlineApiError(Exception):
    pass


class DeadlineApi:
    def __init__(self, deadline_url: str, http_module=requests):
        self._deadline_url = deadline_url
        self._http_module = http_module

    def submit_jobs(self, jobs: List[DeadlineJob]) -> None:
        if not jobs:
            raise DeadlineApiError(f"Jobs can not be empty list or None, was {jobs}")
        url = self._build_jobs_url()

        job_list = self._create_list_of_jobs(jobs)
        data = {"Jobs": job_list}

        logger.debug("Submitting %s job(s) to deadline", len(data))

        response = self._http_module.post(url, json=data)
        self._handle_response_errors(response)

        logger.debug("Submitted %s job(s) to deadline", len(jobs))

    def _handle_response_errors(self, response):
        if response.status_code != 200:
            raise DeadlineApiError(
                f"Error when submitting job to deadline: Error {response.status_code}: {response.text}"
            )

    def _create_list_of_jobs(self, jobs):
        job_list = []
        for job in jobs:
            job_list.append(
                {"JobInfo": job.job_info, "PluginInfo": job.plugin_info, "AuxFiles": []}
            )
        return job_list

    def _build_jobs_url(self):
        return self._deadline_url + "/api/jobs"
