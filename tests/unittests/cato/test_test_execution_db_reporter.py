import datetime

import pytest

from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.image import Image
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.project import Project
from cato_common.domain.run import Run
from cato_common.domain.test_identifier import TestIdentifier
from tests.utils import mock_safe
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    MachineInfoDto,
    StartTestResultDto,
    ComparisonMethodDto,
    ComparisonSettingsDto,
)

SUITES = [
    TestSuite(
        name="my_suite",
        tests=[
            Test(
                name="my_test",
                command="my_command",
                variables={},
                comparison_settings=ComparisonSettings.default(),
            )
        ],
        variables={},
    )
]


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.mock_machine_info_collector = mock_safe(MachineInfoCollector)
            self.mock_machine_info_collector.collect.return_value = MachineInfo(
                cpu_name="my_cpu", cores=8, memory=8
            )
            self.mock_cato_api_client = mock_safe(CatoApiClient)
            self.mock_last_run_information_repository = mock_safe(
                LastRunInformationRepository
            )
            self.test_execution_db_reporter = TestExecutionDbReporter(
                self.mock_machine_info_collector,
                self.mock_cato_api_client,
            )

    return TestContext()


class TestTestExecutionDbReporter:
    def test_start_execution_not_existing_project_should_create(self, test_context):
        test_context.mock_cato_api_client.get_project_by_name.return_value = None

        test_context.test_execution_db_reporter.start_execution(
            "my_project_name", SUITES
        )

        test_context.mock_cato_api_client.create_project.assert_called_with(
            "my_project_name"
        )

    def test_start_execution_should_create_run(self, test_context):
        test_context.mock_cato_api_client.get_project_by_name.return_value = Project(
            id=1, name="my_project_name"
        )
        test_context.mock_cato_api_client.create_run.return_value = Run(
            id=5, project_id=1, started_at=datetime.datetime.now()
        )

        test_context.test_execution_db_reporter.start_execution(
            "my_project_name", SUITES
        )

        test_context.mock_cato_api_client.create_run.assert_called_with(
            CreateFullRunDto(
                1,
                test_suites=[
                    TestSuiteForRunCreation(
                        suite_name="my_suite",
                        tests=[
                            TestForRunCreation(
                                test_command="my_command",
                                test_identifier="my_suite/my_test",
                                test_name="my_test",
                                test_variables={},
                                comparison_settings=ComparisonSettingsDto(
                                    method=ComparisonMethodDto.SSIM, threshold=0.8
                                ),
                            )
                        ],
                        suite_variables={},
                    )
                ],
            )
        )
        assert test_context.test_execution_db_reporter._run_id == 5

    def test_report_test_execution_start_should_report(
        self, test_result_factory, test_context
    ):
        test_context.test_execution_db_reporter._run_id = 5
        test_result = test_result_factory(
            execution_status=ExecutionStatus.NOT_STARTED, started_at=None
        )
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            test_result
        )

        test_context.test_execution_db_reporter.report_test_execution_start(
            SUITES[0], SUITES[0].tests[0]
        )

        test_context.mock_cato_api_client.start_test.assert_called_with(
            StartTestResultDto(
                id=test_result.id,
                machine_info=MachineInfoDto(cpu_name="my_cpu", cores=8, memory=8),
            )
        )

    def test_report_test_execution_start_no_test_result_should_exit(
        self, test_result_factory, test_context
    ):
        test_context.test_execution_db_reporter._run_id = 5
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            None
        )

        test_context.test_execution_db_reporter.report_test_execution_start(
            SUITES[0], SUITES[0].tests[0]
        )

        test_context.mock_cato_api_client.update_test_result.assert_not_called()

    def test_report_test_execution_start_missing_run_id_should_fail(self, test_context):
        with pytest.raises(RuntimeError):
            test_context.test_execution_db_reporter.report_test_execution_start(
                SUITES[0], SUITES[0].tests[0]
            )

    def test_report_heartbeat_should_fail_no_run_id(self, test_context):
        test_identifier = TestIdentifier("my_suite", "my_test")

        with pytest.raises(RuntimeError):
            test_context.test_execution_db_reporter.report_heartbeat(test_identifier)

        test_context.mock_cato_api_client.heartbeat_test.assert_not_called()

    def test_report_heartbeat_should_report(self, test_context):
        test_context.test_execution_db_reporter._run_id = 5
        test_identifier = TestIdentifier("my_suite", "my_test")

        test_context.test_execution_db_reporter.report_heartbeat(test_identifier)

        test_context.mock_cato_api_client.heartbeat_test.assert_called_with(
            5, test_identifier
        )

    def test_report_test_result_should_report(self, test_result_factory, test_context):
        test_context.test_execution_db_reporter._run_id = 5
        test_result = test_result_factory(execution_status=ExecutionStatus.RUNNING)
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            test_result
        )
        test_context.mock_cato_api_client.upload_image = lambda x: Image(
            id=3 if x == "test.exr" else 4,
            name=x,
            original_file_id=4,
            channels=[],
            width=1920,
            height=1080,
        )
        started_at = datetime.datetime.now()
        finished_at = datetime.datetime.now()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=TestStatus.SUCCESS,
            output=["this", "is", "my", "output"],
            seconds=4,
            message="",
            image_output=10,
            reference_image=20,
            diff_image=30,
            started_at=started_at,
            finished_at=finished_at,
            error_value=1,
            failure_reason=None,
        )

        test_context.test_execution_db_reporter.report_test_result(
            SUITES[0], test_execution_result
        )

        test_context.mock_cato_api_client.finish_test.assert_called_with(
            test_result.id,
            status=TestStatus.SUCCESS,
            seconds=4,
            message="",
            image_output=10,
            reference_image=20,
            diff_image=30,
            error_value=1,
            failure_reason=None,
        )
        test_context.mock_cato_api_client.upload_output.assert_called_with(
            test_result.id, "thisismyoutput"
        )

    def test_report_test_result_result_not_found_should_exit(self, test_context):
        test_context.test_execution_db_reporter._run_id = 5
        started_at = datetime.datetime.now()
        finished_at = datetime.datetime.now()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=TestStatus.SUCCESS,
            output=["this", "is", "my", "output"],
            seconds=4,
            message="",
            image_output=10,
            reference_image=20,
            diff_image=30,
            started_at=started_at,
            finished_at=finished_at,
            error_value=1,
            failure_reason=None,
        )
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            None
        )

        test_context.test_execution_db_reporter.report_test_result(
            SUITES[0], test_execution_result
        )

        test_context.mock_cato_api_client.upload_image.assert_not_called()
        test_context.mock_cato_api_client.finish_test.assert_not_called()
        test_context.mock_cato_api_client.upload_output.assert_not_called()

    def test_report_test_result_should_report_without_images(
        self, test_result_factory, test_context
    ):
        test_context.test_execution_db_reporter._run_id = 5
        test_result = test_result_factory(execution_status=ExecutionStatus.RUNNING)
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            test_result
        )
        started_at = datetime.datetime.now()
        finished_at = datetime.datetime.now()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=TestStatus.SUCCESS,
            output=["this", "is", "my", "output"],
            seconds=4,
            message="",
            image_output=None,
            reference_image=None,
            diff_image=None,
            started_at=started_at,
            finished_at=finished_at,
            error_value=1,
            failure_reason=None,
        )

        test_context.test_execution_db_reporter.report_test_result(
            SUITES[0], test_execution_result
        )

        test_context.mock_cato_api_client.finish_test.assert_called_with(
            test_result.id,
            status=TestStatus.SUCCESS,
            seconds=4,
            message="",
            image_output=None,
            reference_image=None,
            diff_image=None,
            error_value=1,
            failure_reason=None,
        )
        test_context.mock_cato_api_client.upload_output.assert_called_with(
            test_result.id, "thisismyoutput"
        )
        test_context.mock_cato_api_client.upload_image.assert_not_called()

    def test_report_test_result_no_run_id_should_fail(self, test_context):
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=TestStatus.SUCCESS,
            output=["this", "is", "my", "output"],
            seconds=4,
            message="",
            image_output=None,
            reference_image=None,
            diff_image=None,
            started_at=datetime.datetime.now(),
            finished_at=datetime.datetime.now(),
            error_value=1,
            failure_reason=None,
        )

        with pytest.raises(RuntimeError):
            test_context.test_execution_db_reporter.report_test_result(
                SUITES[0], test_execution_result
            )

    def test_should_write_last_run_id(self, test_context):
        test_context.test_execution_db_reporter._run_id = 2

        test_context.test_execution_db_reporter.report_test_execution_end(
            test_context.mock_last_run_information_repository
        )

        test_context.mock_last_run_information_repository.write_last_run_information.assert_called_with(
            LastRunInformation(last_run_id=2)
        )

    def test_use_run_id(self, test_context):
        test_context.test_execution_db_reporter.use_run_id(10)

        assert test_context.test_execution_db_reporter._run_id == 10

    def test_use_not_existing_run_id_should_fail(self, test_context):
        test_context.mock_cato_api_client.run_id_exists.return_value = False

        with pytest.raises(ValueError):
            test_context.test_execution_db_reporter.use_run_id(10)

    def test_run_id(self, test_context):
        test_context.test_execution_db_reporter.use_run_id(10)

        assert test_context.test_execution_db_reporter.run_id() == 10
