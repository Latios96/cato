import datetime

import pytest

from cato.domain.test import Test
from cato.domain.test_execution_result import TestExecutionResult
from cato.domain.test_status import TestStatus
from cato.domain.test_suite import TestSuite
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_api_client.cato_api_client import CatoApiClient
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.image import Image
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.project import Project
from cato_server.domain.run import Run
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from tests.utils import mock_safe
from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    MachineInfoDto,
)

SUITES = [
    TestSuite(
        name="my_suite",
        tests=[Test(name="my_test", command="my_command", variables={})],
        variables={},
    )
]


def test_start_execution_not_existing_project_should_create():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    mock_machine_info_collector.collect.return_value = MachineInfo(
        cpu_name="my_cpu", cores=8, memory=8
    )
    mock_cato_api_client.get_project_by_name.return_value = None

    test_execution_db_reporter.start_execution("my_project_name", SUITES)

    mock_cato_api_client.create_project.assert_called_with("my_project_name")


def test_start_execution_should_create_full_run():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    machine_info = MachineInfo(cpu_name="my_cpu", cores=8, memory=8)
    mock_machine_info_collector.collect.return_value = machine_info
    mock_cato_api_client.get_project_by_name.return_value = Project(
        id=1, name="my_project_name"
    )
    mock_cato_api_client.create_full_run.return_value = Run(
        id=5, project_id=1, started_at=datetime.datetime.now()
    )

    test_execution_db_reporter.start_execution("my_project_name", SUITES)

    mock_cato_api_client.create_full_run.assert_called_with(
        CreateFullRunDto(
            1,
            test_suites=[
                TestSuiteForRunCreation(
                    suite_name="my_suite",
                    tests=[
                        TestForRunCreation(
                            machine_info=MachineInfoDto(
                                cpu_name="my_cpu", cores=8, memory=8
                            ),
                            test_command="my_command",
                            test_identifier="my_suite/my_test",
                            test_name="my_test",
                            test_variables={},
                        )
                    ],
                    suite_variables={},
                )
            ],
        )
    )
    assert test_execution_db_reporter._run_id == 5


def test_report_test_execution_start_should_report(test_result_factory):
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    test_result = test_result_factory(
        execution_status=ExecutionStatus.NOT_STARTED, started_at=None
    )
    mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
        test_result
    )

    test_execution_db_reporter.report_test_execution_start(
        SUITES[0], SUITES[0].tests[0]
    )

    mock_cato_api_client.update_test_result.assert_called_with(test_result)
    assert test_result.execution_status == ExecutionStatus.RUNNING
    assert test_result.started_at


def test_report_test_execution_start_no_test_result_should_exit(test_result_factory):
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = None

    test_execution_db_reporter.report_test_execution_start(
        SUITES[0], SUITES[0].tests[0]
    )

    mock_cato_api_client.update_test_result.assert_not_called()


def test_report_test_execution_start_missing_run_id_should_fail():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )

    with pytest.raises(RuntimeError):
        test_execution_db_reporter.report_test_execution_start(
            SUITES[0], SUITES[0].tests[0]
        )


def test_report_heartbeat_should_fail_no_run_id():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_identifier = TestIdentifier("my_suite", "my_test")

    with pytest.raises(RuntimeError):
        test_execution_db_reporter.report_heartbeat(test_identifier)

    mock_cato_api_client.heartbeat_test.assert_not_called()


def test_report_heartbeat_should_report():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    test_identifier = TestIdentifier("my_suite", "my_test")

    test_execution_db_reporter.report_heartbeat(test_identifier)

    mock_cato_api_client.heartbeat_test.assert_called_with(5, test_identifier)


def test_report_test_result_should_report(test_result_factory):
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    test_result = test_result_factory(execution_status=ExecutionStatus.RUNNING)
    mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
        test_result
    )
    mock_cato_api_client.upload_image = lambda x: Image(
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
        image_output="test.exr",
        reference_image="reference.exr",
        started_at=started_at,
        finished_at=finished_at,
    )

    test_execution_db_reporter.report_test_result(SUITES[0], test_execution_result)

    mock_cato_api_client.finish_test.assert_called_with(
        test_result.id,
        status=TestStatus.SUCCESS,
        seconds=4,
        message="",
        image_output=3,
        reference_image=4,
    )
    mock_cato_api_client.upload_output.assert_called_with(
        test_result.id, "thisismyoutput"
    )


def test_report_test_result_result_not_found_should_exit():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    test_execution_result = TestExecutionResult(
        test=SUITES[0].tests[0],
        status=TestStatus.SUCCESS,
        output=["this", "is", "my", "output"],
        seconds=4,
        message="",
        image_output="test.exr",
        reference_image="reference.exr",
        started_at=started_at,
        finished_at=finished_at,
    )
    mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = None

    test_execution_db_reporter.report_test_result(SUITES[0], test_execution_result)

    mock_cato_api_client.upload_image.assert_not_called()
    mock_cato_api_client.finish_test.assert_not_called()
    mock_cato_api_client.upload_output.assert_not_called()


def test_report_test_result_should_report_without_images(test_result_factory):
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_db_reporter._run_id = 5
    test_result = test_result_factory(execution_status=ExecutionStatus.RUNNING)
    mock_cato_api_client.find_test_result_by_run_id_and_identifier.return_value = (
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
        started_at=started_at,
        finished_at=finished_at,
    )

    test_execution_db_reporter.report_test_result(SUITES[0], test_execution_result)

    mock_cato_api_client.finish_test.assert_called_with(
        test_result.id,
        status=TestStatus.SUCCESS,
        seconds=4,
        message="",
        image_output=None,
        reference_image=None,
    )
    mock_cato_api_client.upload_output.assert_called_with(
        test_result.id, "thisismyoutput"
    )
    mock_cato_api_client.upload_image.assert_not_called()


def test_report_test_result_no_run_id_should_fail():
    mock_machine_info_collector = mock_safe(MachineInfoCollector)
    mock_cato_api_client = mock_safe(CatoApiClient)
    test_execution_db_reporter = TestExecutionDbReporter(
        mock_machine_info_collector, mock_cato_api_client
    )
    test_execution_result = TestExecutionResult(
        test=SUITES[0].tests[0],
        status=TestStatus.SUCCESS,
        output=["this", "is", "my", "output"],
        seconds=4,
        message="",
        image_output=None,
        reference_image=None,
        started_at=datetime.datetime.now(),
        finished_at=datetime.datetime.now(),
    )

    with pytest.raises(RuntimeError):
        test_execution_db_reporter.report_test_result(SUITES[0], test_execution_result)
