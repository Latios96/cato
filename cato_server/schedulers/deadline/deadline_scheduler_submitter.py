import logging
from typing import List

from cato.domain.test_suite import iterate_suites_and_tests
from cato_common.domain.submission_info import SubmissionInfo
from cato_server.schedulers.deadline.deadline_api import DeadlineApi
from cato_server.schedulers.deadline.deadline_job import DeadlineJob

logger = logging.getLogger(__name__)


class DeadlineSchedulerSubmitter:
    def __init__(self, deadline_url, deadline_api: DeadlineApi):
        self._deadline_url = deadline_url
        self._deadline_api = deadline_api

    def submit_tests(self, submission_info: SubmissionInfo) -> None:
        jobs = []
        for suite, test in iterate_suites_and_tests(submission_info.config.suites):
            job = self._create_job(submission_info, suite, test)
            jobs.append(job)

        logger.info("Submitting %s jobs to Deadline..", len(jobs))
        self._deadline_api.submit_jobs(jobs)
        logger.info("Successfully submitted %s jobs to Deadline", len(jobs))

    def _create_job(self, submission_info, suite, test) -> DeadlineJob:
        job_info = self._create_job_info(submission_info, suite, test)
        plugin_info = self._create_plugin_info(submission_info, suite, test)

        return DeadlineJob(job_info, plugin_info)

    def _create_job_info(self, submission_info, suite, test):
        return {
            "Plugin": "CommandLine",
            "Name": test.name,
            "BatchName": f"{submission_info.config.project_name} Run #{submission_info.run_id} {suite.name} ",
        }

    def _create_plugin_info(self, submission_info, suite, test):
        test_identifier_str = f"{suite.name}/{test.name}"
        command = self._create_command(submission_info, test_identifier_str)

        plugin_info = {
            "Arguments": " ".join(command),
            "Executable": submission_info.executable,
            "Shell": "default",
            "ShellExecute": "False",
            "SingleFramesOnly": "True",
            "StartupDirectory": submission_info.resource_path,
        }

        return plugin_info

    def _create_command(
        self, submission_info: SubmissionInfo, test_identifier_str: str
    ) -> List[str]:
        command = [
            "-m",
            "cato",
            "worker-run",
            "-u",
            "http://localhost:5000",  # todo get from config
            "-submission-info-id",
            "{}".format(submission_info.id),
            "-test-identifier",
            '"{}"'.format(test_identifier_str),
        ]
        return command
