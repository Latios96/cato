import pytest

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_execution_result import TestExecutionResult
from cato_common.domain.test_suite import TestSuite
from cato.file_system_abstractions.last_run_information_repository import (
    LastRunInformationRepository,
    LastRunInformation,
)
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.utils.branch_detector import BranchDetector
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_api_client.cato_api_client import CatoApiClient
from cato_common.domain.branch_name import BranchName
from cato_common.domain.image import Image
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.project import Project
from cato_common.domain.run import Run
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.create_full_run_dto import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
)
from cato_common.dtos.start_test_result_dto import StartTestResultDto
from cato_common.utils.datetime_utils import aware_now_in_utc
from tests.utils import mock_safe

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
            self.mock_branch_detector = mock_safe(BranchDetector)
            self.mock_branch_detector.detect_branch.return_value = None
            self.test_execution_db_reporter = TestExecutionDbReporter(
                self.mock_machine_info_collector,
                self.mock_cato_api_client,
                self.mock_branch_detector,
            )

    return TestContext()


class TestTestExecutionDbReporter:
    def test_start_execution_not_existing_project_should_create(self, test_context):
        test_context.mock_cato_api_client.get_project_by_name.return_value = None

        test_context.test_execution_db_reporter.start_execution(
            RunConfig(
                project_name="my_project_name",
                resource_path="test",
                suites=SUITES,
                output_folder="testoutput",
                variables={},
            )
        )

        test_context.mock_cato_api_client.create_project.assert_called_with(
            "my_project_name"
        )

    def test_start_execution_should_create_run_with_branch_name(self, test_context):
        test_context.mock_branch_detector.detect_branch.return_value = BranchName(
            "my_branch"
        )
        test_context.mock_cato_api_client.get_project_by_name.return_value = Project(
            id=1, name="my_project_name"
        )
        test_context.mock_cato_api_client.create_run.return_value = Run(
            id=5,
            project_id=1,
            run_batch_id=42,
            started_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=None,
        )

        test_context.test_execution_db_reporter.start_execution(
            RunConfig(
                project_name="my_project_name",
                resource_path="test",
                suites=SUITES,
                output_folder="testoutput",
                variables={},
            )
        )

        test_context.mock_cato_api_client.create_run.assert_called_with(
            CreateFullRunDto(
                project_id=1,
                test_suites=[
                    TestSuiteForRunCreation(
                        suite_name="my_suite",
                        tests=[
                            TestForRunCreation(
                                test_command="my_command",
                                test_identifier=TestIdentifier.from_string(
                                    "my_suite/my_test"
                                ),
                                test_name="my_test",
                                test_variables={},
                                comparison_settings=ComparisonSettings.default(),
                            )
                        ],
                        suite_variables={},
                    )
                ],
                branch_name=BranchName("my_branch"),
            )
        )
        assert test_context.test_execution_db_reporter._run_id == 5

    def test_start_execution_should_not_pass_branch_name_if_there_is_no_branch(
        self, test_context
    ):
        test_context.mock_cato_api_client.get_project_by_name.return_value = Project(
            id=1, name="my_project_name"
        )
        test_context.mock_cato_api_client.create_run.return_value = Run(
            id=5,
            project_id=1,
            run_batch_id=42,
            started_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=None,
        )

        test_context.test_execution_db_reporter.start_execution(
            RunConfig(
                project_name="my_project_name",
                resource_path="test",
                suites=SUITES,
                output_folder="testoutput",
                variables={},
            )
        )

        assert (
            test_context.mock_cato_api_client.create_run.call_args[0][0].branch_name
            is None
        )

    def test_report_test_execution_start_should_report(
        self, test_result_factory, test_context
    ):
        test_context.test_execution_db_reporter._run_id = 5
        test_result = test_result_factory(
            unified_test_status=UnifiedTestStatus.NOT_STARTED, started_at=None
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
                machine_info=MachineInfo(cpu_name="my_cpu", cores=8, memory=8),
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
        test_result = test_result_factory(unified_test_status=UnifiedTestStatus.RUNNING)
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
        started_at = aware_now_in_utc()
        finished_at = aware_now_in_utc()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=ResultStatus.SUCCESS,
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
            status=ResultStatus.SUCCESS,
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
        started_at = aware_now_in_utc()
        finished_at = aware_now_in_utc()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=ResultStatus.SUCCESS,
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
        test_result = test_result_factory(unified_test_status=UnifiedTestStatus.RUNNING)
        test_context.mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
            test_result
        )
        started_at = aware_now_in_utc()
        finished_at = aware_now_in_utc()
        test_execution_result = TestExecutionResult(
            test=SUITES[0].tests[0],
            status=ResultStatus.SUCCESS,
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
            status=ResultStatus.SUCCESS,
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
            status=ResultStatus.SUCCESS,
            output=["this", "is", "my", "output"],
            seconds=4,
            message="",
            image_output=None,
            reference_image=None,
            diff_image=None,
            started_at=aware_now_in_utc(),
            finished_at=aware_now_in_utc(),
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
