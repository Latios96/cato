import requests

from cato.config.config_encoder import ConfigEncoder
from cato.config.config_file_parser import JsonConfigParser
from cato.domain.test import Test
from cato_server.schedulers.abstract_scheduler_submitter import SubmissionInfo
from cato_server.schedulers.deadline.deadline_api import DeadlineApi
from cato_server.schedulers.deadline.deadline_job import DeadlineJob
from cato_server.schedulers.deadline.deadline_scheduler_submitter import (
    DeadlineSchedulerSubmitter,
)
from tests.utils import mock_safe


class TestDeadlineSchedulerSubmitter:
    def setup_method(self, method):
        self.config_encoder_mock = mock_safe(ConfigEncoder)
        self.config_encoder_mock.encode.return_value = b"UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms="
        self.deadline_api_mock = mock_safe(DeadlineApi)
        self.deadline_submitter = DeadlineSchedulerSubmitter(
            self.config_encoder_mock, "http://localhost:8085", self.deadline_api_mock
        )

    def test_should_submit_single_job_successfully(self, config_fixture):
        submission_info = SubmissionInfo(
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
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -config UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms= -test-identifier "My_first_test_Suite/My_first_test" -run-id 42 -resource-path "my/resource/folder"',
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
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -config UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms= -test-identifier "My_first_test_Suite/My_first_test" -run-id 42 -resource-path "my/resource/folder"',
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
                        "Arguments": '-m cato worker-run -u http://localhost:5000 -config UG9seWZvbiB6d2l0c2NoZXJuZCBhw59lbiBNw6R4Y2hlbnMgVsO2Z2VsIFLDvGJlbiwgSm9naHVydCB1bmQgUXVhcms= -test-identifier "My_first_test_Suite/AnotherTest" -run-id 42 -resource-path "my/resource/folder"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                ),
            ]
        )
