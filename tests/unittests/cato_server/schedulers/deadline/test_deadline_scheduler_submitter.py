from cato.domain.test import Test
from cato_server.domain.submission_info import SubmissionInfo
from cato_server.schedulers.deadline.deadline_api import DeadlineApi
from cato_server.schedulers.deadline.deadline_job import DeadlineJob
from cato_server.schedulers.deadline.deadline_scheduler_submitter import (
    DeadlineSchedulerSubmitter,
)
from tests.utils import mock_safe


class TestDeadlineSchedulerSubmitter:
    def setup_method(self, method):
        self.deadline_api_mock = mock_safe(DeadlineApi)
        self.deadline_submitter = DeadlineSchedulerSubmitter(
            "http://localhost:8085", self.deadline_api_mock
        )

    def test_should_submit_single_job_successfully(self, config_fixture):
        submission_info = SubmissionInfo(
            id=0,
            config=config_fixture.CONFIG,
            run_id=42,
            resource_path="my/resource/folder",
            executable="python",
        )

        self.deadline_submitter.submit_tests(submission_info)

        self.deadline_api_mock.submit_jobs.assert_called_with(
            [
                DeadlineJob(
                    job_info={
                        "Plugin": "CommandLine",
                        "Name": "My_first_test",
                        "BatchName": "EXAMPLE_PROJECT Run #42 My_first_test_Suite ",
                    },
                    plugin_info={
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -submission-info-id 0 -test-identifier "My_first_test_Suite/My_first_test"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                )
            ]
        )

    def test_should_submit_all_jobs(self, config_fixture):
        config = config_fixture.CONFIG
        config.test_suites[0].tests.append(
            Test(
                name="AnotherTest",
                command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                variables={"frame": "7"},
            )
        )
        submission_info = SubmissionInfo(
            id=0,
            config=config_fixture.CONFIG,
            run_id=42,
            resource_path="my/resource/folder",
            executable="python",
        )

        self.deadline_submitter.submit_tests(submission_info)

        self.deadline_api_mock.submit_jobs.assert_called_with(
            [
                DeadlineJob(
                    job_info={
                        "Plugin": "CommandLine",
                        "Name": "My_first_test",
                        "BatchName": "EXAMPLE_PROJECT Run #42 My_first_test_Suite ",
                    },
                    plugin_info={
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -submission-info-id 0 -test-identifier "My_first_test_Suite/My_first_test"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                ),
                DeadlineJob(
                    job_info={
                        "Plugin": "CommandLine",
                        "Name": "AnotherTest",
                        "BatchName": "EXAMPLE_PROJECT Run #42 My_first_test_Suite ",
                    },
                    plugin_info={
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -submission-info-id 0 -test-identifier "My_first_test_Suite/AnotherTest"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                ),
            ]
        )
