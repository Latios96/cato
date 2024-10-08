import datetime
import os

import pytest

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_api_client.task_result_template import TaskResultError
from cato_common.domain.branch_name import BranchName
from cato_common.domain.compare_image_result import CompareImageResult
from cato_common.domain.file import File
from cato_common.domain.image import Image, ImageChannel, ImageTranscodingState
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.output import Output
from cato_common.domain.project import Project, ProjectStatus
from cato_common.domain.result_status import ResultStatus
from cato_common.domain.run_information import OS
from cato_common.domain.submission_info import SubmissionInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.dtos.create_full_run_dto import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    LocalComputerRunInformationForRunCreation,
)
from cato_common.dtos.start_test_result_dto import StartTestResultDto
from cato_common.utils.datetime_utils import aware_now_in_utc


def test_get_project_by_name_should_get_project(cato_api_client, project):
    project = cato_api_client.get_project_by_name("test_name")

    assert project == Project(1, "test_name", status=ProjectStatus.ACTIVE)


def test_get_project_by_name_should_get_none(cato_api_client):
    project = cato_api_client.get_project_by_name("ysdf")

    assert project is None


def test_create_project_should_create_project(cato_api_client):
    project = cato_api_client.create_project("my_project")

    assert project == Project(id=1, name="my_project", status=ProjectStatus.ACTIVE)


def test_create_project_should_not_create_invalid_name(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.create_project("my%&&&project")


def test_upload_file(cato_api_client, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client.upload_file(path)

    assert f == File(
        id=1,
        name="test.exr",
        hash="a233c347f49d2745b4f759bec0da9414e1bc980b1ece56f98dd7f9696d608709",
        value_counter=0,
    )


def test_upload_file_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_file(path)


def test_get_test_result_by_run_and_identifier_success(
    cato_api_client, suite_result, test_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        suite_result.run_id,
        TestIdentifier(suite_result.suite_name, test_result.test_name),
    )

    assert result == TestResult(
        id=1,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test_name"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="success",
        image_output=1,
        reference_image=1,
        diff_image=1,
        started_at=test_result.started_at,
        finished_at=test_result.finished_at,
    )


def test_get_test_result_by_run_and_identifier_should_fail_invalid_run_id(
    cato_api_client, suite_result, test_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        10, TestIdentifier(suite_result.suite_name, test_result.test_name)
    )

    assert result is None


def test_get_test_result_by_run_and_identifier_should_fail_invalid_test_identifier(
    cato_api_client, suite_result
):
    result = cato_api_client.find_test_result_by_run_id_and_identifier(
        suite_result.run_id, TestIdentifier("test", "wurst")
    )

    assert result is None


def test_upload_output_success(cato_api_client, test_result):
    output = cato_api_client.upload_output(test_result.id, "my text")

    assert output == Output(id=1, test_result_id=test_result.id, text="my text")


def test_upload_output_failure(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.upload_output(42, "my text")


def test_upload_performance_trace_success(cato_api_client, run):
    performance_trace_id = cato_api_client.upload_performance_trace(
        run.id, """{"traceEvents":[]}"""
    )

    assert performance_trace_id == 1


def test_upload_performance_trace_failure(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.upload_performance_trace(1, """{"traceEvents":[]}""")


def test_upload_image(cato_api_client, test_resource_provider):
    path = test_resource_provider.resource_by_name("test.exr")

    f = cato_api_client.upload_image(path)

    assert f == Image(
        id=1,
        name="test.exr",
        original_file_id=1,
        channels=[],
        width=0,
        height=0,
        transcoding_state=ImageTranscodingState.WAITING_FOR_TRANSCODING,
    )


def test_upload_image_async_not_existing(cato_api_client):
    path = os.path.join(os.path.dirname(__file__), "seAERER")

    with pytest.raises(ValueError):
        cato_api_client.upload_image(path)


def test_create_run_success(cato_api_client, project, run_batch_identifier):
    dto = CreateFullRunDto(
        project_id=project.id,
        run_batch_identifier=run_batch_identifier,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        test_command="cmd",
                        test_identifier=TestIdentifier.from_string("test/identifier"),
                        test_name="test_name",
                        test_variables={},
                        comparison_settings=ComparisonSettings.default(),
                    )
                ],
            )
        ],
        run_information=LocalComputerRunInformationForRunCreation(
            os=OS.WINDOWS, computer_name="cray", local_username="username"
        ),
        branch_name=BranchName("default"),
    )
    run = cato_api_client.create_run(dto)
    assert run.id == project.id


def test_create_run_failure(cato_api_client, run_batch_identifier):
    dto = CreateFullRunDto(
        project_id=42,
        run_batch_identifier=run_batch_identifier,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        test_command="cmd",
                        test_identifier=TestIdentifier.from_string("test/identifier"),
                        test_name="test_name",
                        test_variables={},
                        comparison_settings=ComparisonSettings.default(),
                    )
                ],
            )
        ],
        run_information=LocalComputerRunInformationForRunCreation(
            os=OS.WINDOWS, computer_name="cray", local_username="username"
        ),
        branch_name=BranchName("default"),
    )
    with pytest.raises(ValueError):
        cato_api_client.create_run(dto)


def test_send_test_heartbeat(cato_api_client, run, test_result):
    cato_api_client.heartbeat_test(run.id, test_result.test_identifier)


def test_send_test_heartbeat_not_existing_test_id(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.heartbeat_test(42, TestIdentifier("suite_name", "test_name"))


def test_finish_test_result_success(cato_api_client, test_result, stored_image_factory):
    cato_api_client.finish_test(
        test_result_id=test_result.id,
        status=ResultStatus.SUCCESS,
        seconds=3,
        message="my_mesage",
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
        diff_image=stored_image_factory().id,
    )


def test_finish_test_result_failure(cato_api_client, test_result, stored_image):
    with pytest.raises(ValueError):
        cato_api_client.finish_test(
            test_result_id=test_result.id,
            status=ResultStatus.SUCCESS,
            seconds=3,
            message="my_mesage",
            image_output=42,
            reference_image=stored_image.id,
            failure_reason=TestFailureReason.TIMED_OUT,
        )


def test_get_test_results_by_run_id_and_test_status_should_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, UnifiedTestStatus.NOT_STARTED
    )

    assert identifiers == [test_result.test_identifier]


def test_get_test_results_by_run_id_and_test_status_should_not_find(
    cato_api_client, run, test_result
):
    identifiers = cato_api_client.get_test_results_by_run_id_and_test_status(
        run.id, ResultStatus.FAILED
    )

    assert identifiers == []


def test_run_id_exists_success(cato_api_client, run):
    assert cato_api_client.run_id_exists(run.id)


def test_run_id_exists_failure(cato_api_client):
    assert not cato_api_client.run_id_exists(42)


def test_submit_to_scheduler_success(cato_api_client, config_fixture, run):
    submission_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=run.id,
        resource_path="resource_path",
        executable=r"python.exe",
    )

    cato_api_client.submit_to_scheduler(submission_info)


def test_find_submission_info_by_id(cato_api_client, submission_info):
    found_info = cato_api_client.get_submission_info_by_id(submission_info.id)

    assert found_info == submission_info


def test_find_submission_info_by_not_existing_id(cato_api_client):
    found_info = cato_api_client.get_submission_info_by_id(42)

    assert found_info == None


def test_start_test_success(cato_api_client, test_result):
    cato_api_client.start_test(
        StartTestResultDto(
            id=test_result.id,
            machine_info=MachineInfo(cpu_name="Intel", cores=1, memory=1),
        )
    )


def test_start_test_failure(cato_api_client):
    with pytest.raises(ValueError):
        cato_api_client.start_test(
            StartTestResultDto(
                id=43, machine_info=MachineInfo(cpu_name="Intel", cores=1, memory=1)
            )
        )


def test_compare_images_success(cato_api_client, test_resource_provider):
    result = cato_api_client.compare_images(
        test_resource_provider.resource_by_name("test_image_white.jpg"),
        test_resource_provider.resource_by_name("test_image_white.jpg"),
        ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
    )

    assert result == CompareImageResult(
        status=ResultStatus.SUCCESS,
        message=None,
        reference_image_id=2,
        output_image_id=1,
        diff_image_id=3,
        error=1,
    )


def test_compare_images_success_should_fail_for_not_existing_reference_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(ValueError):
        cato_api_client.compare_images(
            "not_existing.jpg",
            test_resource_provider.resource_by_name("test_image_black.png"),
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_compare_images_success_should_fail_for_not_existing_output_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(ValueError):
        cato_api_client.compare_images(
            test_resource_provider.resource_by_name("test_image_black.png"),
            "not_existing.jpg",
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_compare_images_success_should_fail_for_non_image(
    cato_api_client, test_resource_provider
):
    with pytest.raises(TaskResultError):
        cato_api_client.compare_images(
            test_resource_provider.resource_by_name("unsupported-file.txt"),
            test_resource_provider.resource_by_name("unsupported-file.txt"),
            ComparisonSettings(method=ComparisonMethod.SSIM, threshold=1),
        )


def test_get_test_edits_to_sync_for_run_should_return_edits(
    cato_api_client,
    run,
    test_result,
    saving_comparison_settings_edit_factory,
    saving_reference_image_edit_factory,
):
    comparison_settings_edit = saving_comparison_settings_edit_factory(
        test_id=test_result.id,
        created_at=aware_now_in_utc() - datetime.timedelta(seconds=10),
    )
    reference_image_edit = saving_reference_image_edit_factory(
        test_id=test_result.id, created_at=aware_now_in_utc()
    )
    edits = cato_api_client.get_test_edits_to_sync_for_run(run.id)

    assert edits == [comparison_settings_edit, reference_image_edit]


def test_get_test_edits_to_sync_for_run_should_return_empty_list(cato_api_client, run):
    edits = cato_api_client.get_test_edits_to_sync_for_run(run.id)

    assert edits == []


def test_download_original_image_success(cato_api_client, stored_image):
    content = cato_api_client.download_original_image(stored_image.id)

    assert len(content) == 87444


def test_download_original_image_not_found(cato_api_client):
    content = cato_api_client.download_original_image(1)

    assert content is None


def test_get_image_by_id_success(cato_api_client, stored_image):
    image = cato_api_client.get_image_by_id(stored_image.id)

    assert image == stored_image


def test_get_image_by_id_not_found(cato_api_client):
    image = cato_api_client.get_image_by_id(42)

    assert image is None
