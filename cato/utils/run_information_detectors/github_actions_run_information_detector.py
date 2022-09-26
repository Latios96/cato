from typing import cast

import requests

from cato.utils.run_information_detectors.abstract_detector import AbstractDetector
from cato_common.dtos.create_full_run_dto import (
    BasicRunInformationForRunCreation,
    GithubActionsRunInformationForRunCreation,
)


class GithubActionsRunInformationDetector(AbstractDetector):
    def can_detect(self) -> bool:
        return self._environment.get("GITHUB_ACTIONS") is not None

    def detect(self) -> BasicRunInformationForRunCreation:
        basic_run = super(GithubActionsRunInformationDetector, self).detect()

        github_run_id = int(self._environment["GITHUB_RUN_ID"])
        html_url = self._get_job_html_url()
        job_name = self._environment["GITHUB_JOB"]
        actor = self._environment["GITHUB_ACTOR"]
        attempt = int(self._environment["GITHUB_RUN_ATTEMPT"])
        run_number = int(self._environment["GITHUB_RUN_NUMBER"])
        github_url = self._environment["GITHUB_SERVER_URL"]
        github_api_url = self._environment["GITHUB_API_URL"]

        return GithubActionsRunInformationForRunCreation.from_basic_run(
            basic_run,
            github_run_id=github_run_id,
            html_url=html_url,
            job_name=job_name,
            actor=actor,
            attempt=attempt,
            run_number=run_number,
            github_url=github_url,
            github_api_url=github_api_url,
        )

    def _get_job_html_url(self) -> str:
        github_api_url = self._environment["GITHUB_API_URL"]
        repository = self._environment["GITHUB_REPOSITORY"]
        run_id = self._environment["GITHUB_RUN_ID"]
        url = f"{github_api_url}/repos/{repository}/actions/runs/{run_id}/jobs?per_page=30"
        response = requests.get(
            url,
            headers={
                "Authorization": f"token {self._environment['GITHUB_TOKEN']}",
                "Accept": "application/vnd.github.v3+json",
            },
        )
        if not response.status_code == 200:
            raise RuntimeError(
                f"Error when retriving html url, expected status code 200, was {response.status_code}: {response.text}"
            )
        response_json = response.json()
        jobs = response_json["jobs"]
        job = self._find_job_by_name(jobs, self._environment["GITHUB_JOB"])
        return cast(str, job["html_url"])

    def _find_job_by_name(self, jobs, job_name):
        for job in jobs:
            if job["name"].startswith(job_name):
                return job
        raise ValueError(f"No job with name '{job_name}' found.")
