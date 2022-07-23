import pytest

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test
from cato_common.domain.submission_info import SubmissionInfo
from cato_server.configuration.app_configuration_defaults import (
    AppConfigurationDefaults,
)
from cato_server.schedulers.deadline.deadline_api import DeadlineApi
from cato_server.schedulers.deadline.deadline_job import DeadlineJob
from cato_server.schedulers.deadline.deadline_scheduler_submitter import (
    DeadlineSchedulerSubmitter,
)
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.deadline_api_mock = mock_safe(DeadlineApi)
            self.deadline_submitter = DeadlineSchedulerSubmitter(
                "http://localhost:8085",
                self.deadline_api_mock,
                AppConfigurationDefaults().create(),
            )

    return TestContext()


class TestDeadlineSchedulerSubmitter:
    def test_should_submit_single_job_successfully(self, config_fixture, test_context):
        submission_info = SubmissionInfo(
            id=0,
            config=config_fixture.CONFIG,
            run_id=42,
            resource_path="my/resource/folder",
            executable="python",
        )

        test_context.deadline_submitter.submit_tests(submission_info)

        test_context.deadline_api_mock.submit_jobs.assert_called_with(
            [
                DeadlineJob(
                    job_info={
                        "Plugin": "CommandLine",
                        "Name": "My_first_test",
                        "BatchName": "EXAMPLE_PROJECT Run #42 My_first_test_Suite ",
                    },
                    plugin_info={
                        "Arguments": '-m cato worker-run -u http://127.0.0.1 -submission-info-id 0 -test-identifier "My_first_test_Suite/My_first_test"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                )
            ]
        )

    def test_should_submit_all_jobs(self, config_fixture, test_context):
        config = config_fixture.CONFIG
        config.suites[0].tests.append(
            Test(
                name="AnotherTest",
                command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                variables={"frame": "7"},
                comparison_settings=ComparisonSettings.default(),
            )
        )
        submission_info = SubmissionInfo(
            id=0,
            config=config_fixture.CONFIG,
            run_id=42,
            resource_path="my/resource/folder",
            executable="python",
        )

        test_context.deadline_submitter.submit_tests(submission_info)

        test_context.deadline_api_mock.submit_jobs.assert_called_with(
            [
                DeadlineJob(
                    job_info={
                        "Plugin": "CommandLine",
                        "Name": "My_first_test",
                        "BatchName": "EXAMPLE_PROJECT Run #42 My_first_test_Suite ",
                    },
                    plugin_info={
                        "Arguments": '-m cato worker-run -u http://127.0.0.1 -submission-info-id 0 -test-identifier "My_first_test_Suite/My_first_test"',
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
                        "Arguments": '-m cato worker-run -u http://127.0.0.1 -submission-info-id 0 -test-identifier "My_first_test_Suite/AnotherTest"',
                        "Executable": "python",
                        "Shell": "default",
                        "ShellExecute": "False",
                        "SingleFramesOnly": "True",
                        "StartupDirectory": "my/resource/folder",
                    },
                ),
            ]
        )
