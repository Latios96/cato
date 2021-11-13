import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.storage.page import PageRequest, Page
from cato_server.domain.test_result_status_information import (
    TestResultStatusInformation,
)
from cato_server.storage.abstract.status_filter import StatusFilter
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)


def test_save_success(
    sessionmaker_fixture, suite_result, stored_image_factory, stored_file
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
        diff_image=stored_image_factory().id,
        started_at=start_time,
        finished_at=end_time,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
        error_value=0.5,
        thumbnail_file_id=stored_file.id,
        failure_reason=TestFailureReason.EXIT_CODE_NON_ZERO,
    )

    test_result_save = repository.save(test_result)

    test_result.id = test_result_save.id

    assert test_result_save == test_result


def test_save_with_success_no_failure_reason(
    sessionmaker_fixture, suite_result, stored_image_factory, stored_file
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
        diff_image=stored_image_factory().id,
        started_at=start_time,
        finished_at=end_time,
        comparison_settings=ComparisonSettings(
            method=ComparisonMethod.SSIM, threshold=1
        ),
        error_value=0.5,
        thumbnail_file_id=stored_file.id,
        failure_reason=None,
    )

    test_result_save = repository.save(test_result)

    test_result.id = test_result_save.id

    assert test_result_save == test_result


def test_save_success_no_machine_info_no_comparison_settings(
    sessionmaker_fixture, suite_result, stored_image_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=None,
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image_factory().id,
        reference_image=stored_image_factory().id,
        diff_image=stored_image_factory().id,
        started_at=start_time,
        finished_at=end_time,
    )

    test_result_save = repository.save(test_result)

    test_result.id = test_result_save.id

    assert test_result_save == test_result


def test_save_no_suite_result(sessionmaker_fixture, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=0,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    with pytest.raises(IntegrityError):
        repository.save(test_result)


def test_find_by_suite_result_and_test_identifier(
    sessionmaker_fixture, suite_result, stored_image
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    test_result_save = repository.save(test_result)

    result = repository.find_by_suite_result_and_test_identifier(
        suite_result.id, TestIdentifier("my_suite", "my_test")
    )

    assert result.id == test_result_save.id


def test_find_find_by_suite_result_and_test_identifier_not_found(sessionmaker_fixture):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert not repository.find_by_suite_result_and_test_identifier(
        3, TestIdentifier("my_suite", "my_test")
    )


def test_find_by_suite_result(sessionmaker_fixture, suite_result, stored_image):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    end_time = datetime.datetime.now()
    test_result = TestResult(
        id=0,
        suite_result_id=suite_result.id,
        test_name="my_test_name",
        test_identifier=TestIdentifier(suite_name="my_suite", test_name="my_test"),
        test_command="my_command",
        test_variables={"testkey": "test_value"},
        machine_info=MachineInfo(cpu_name="cpu", cores=56, memory=8),
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        seconds=5,
        message="sucess",
        image_output=stored_image.id,
        reference_image=stored_image.id,
        started_at=start_time,
        finished_at=end_time,
    )
    test_result_save = repository.save(test_result)

    results = repository.find_by_suite_result_id(suite_result.id)

    assert results == [test_result_save]


def test_find_by_suite_result_not_found(sessionmaker_fixture, suite_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_suite_result_id(suite_result.id)

    assert results == []


def test_find_by_run_id_should_find_single_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_run_id(run.id)

    assert results == [test_result]


def test_find_by_run_id_should_find_multiple(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result1 = repository.save(test_result)
    test_result.id = 0
    test_result2 = repository.save(test_result)
    test_result.id = 0
    test_result3 = repository.save(test_result)
    test_result.id = 1

    results = repository.find_by_run_id(run.id)

    assert results == [test_result, test_result1, test_result2, test_result3]


def test_find_by_run_id_should_find_empty_list(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_run_id(run.id)

    assert results == []


def test_find_by_run_id_should_return_correct_order(
    sessionmaker_fixture, run, suite_result, order_test_data, test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    for name in order_test_data.wrong_order:
        repository.save(
            test_result_factory(
                test_identifier=f"{suite_result.suite_name}/{name}",
                test_name=name,
                suite_result_id=suite_result.id,
            )
        )

    results = repository.find_by_run_id(run.id)
    names = list(map(lambda x: x.test_name.lower(), results))

    assert names == order_test_data.correct_order_lowercase


@pytest.fixture
def __status_filter_test_results(
    sessionmaker_fixture, test_result_factory, suite_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    repository.save(
        test_result_factory(
            unified_test_status=UnifiedTestStatus.NOT_STARTED,
            suite_result_id=suite_result.id,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.SUCCESS,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.FAILED,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.NOT_STARTED,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.RUNNING,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.FAILED,
            failure_reason=TestFailureReason.TIMED_OUT,
        )
    )
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.FAILED,
            failure_reason=TestFailureReason.REFERENCE_IMAGE_MISSING,
        )
    )


@pytest.mark.parametrize(
    "filter_by,ids",
    [
        (StatusFilter.NONE, [1, 2, 3, 4, 5, 6, 7]),
        (StatusFilter.NOT_STARTED, [1, 4]),
        (StatusFilter.RUNNING, [5]),
        (StatusFilter.FAILED, [3, 6, 7]),
        (StatusFilter.SUCCESS, [2]),
    ],
)
def test_find_by_run_id_with_filter_options_should_find_correctly(
    sessionmaker_fixture,
    run,
    suite_result,
    __status_filter_test_results,
    filter_by,
    ids,
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id(
        run.id, TestResultFilterOptions(status=filter_by, failure_reason=None)
    )

    assert [x.id for x in result] == ids


@pytest.mark.parametrize(
    "filter_by,ids",
    [
        (TestFailureReason.TIMED_OUT, [6]),
        (TestFailureReason.REFERENCE_IMAGE_MISSING, [7]),
        (TestFailureReason.EXIT_CODE_NON_ZERO, []),
    ],
)
def test_find_by_run_id_with_filter_options_with_failure_reason_should_find_correctly(
    sessionmaker_fixture,
    run,
    suite_result,
    __status_filter_test_results,
    filter_by,
    ids,
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id(
        run.id,
        TestResultFilterOptions(status=StatusFilter.FAILED, failure_reason=filter_by),
    )

    assert [x.id for x in result] == ids


@pytest.mark.parametrize(
    "filter_by,ids",
    [
        (StatusFilter.NONE, [1, 2, 3, 4, 5, 6, 7]),
        (StatusFilter.NOT_STARTED, [1, 4]),
        (StatusFilter.RUNNING, [5]),
        (StatusFilter.FAILED, [3, 6, 7]),
        (StatusFilter.SUCCESS, [2]),
    ],
)
def test_find_by_run_id_paginated_with_filter_options_should_find_correctly(
    sessionmaker_fixture,
    run,
    suite_result,
    __status_filter_test_results,
    filter_by,
    ids,
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result_paginated = repository.find_by_run_id_with_paging(
        run.id,
        PageRequest(1, 10),
        TestResultFilterOptions(status=filter_by, failure_reason=None),
    )

    assert [x.id for x in result_paginated.entities] == ids


@pytest.mark.parametrize(
    "filter_by,ids",
    [
        (TestFailureReason.TIMED_OUT, [6]),
        (TestFailureReason.REFERENCE_IMAGE_MISSING, [7]),
        (TestFailureReason.EXIT_CODE_NON_ZERO, []),
    ],
)
def test_find_by_run_id_paginated_with_filter_options_with_failure_reason_should_find_correctly(
    sessionmaker_fixture,
    run,
    suite_result,
    __status_filter_test_results,
    filter_by,
    ids,
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result_paginated = repository.find_by_run_id_with_paging(
        run.id,
        PageRequest(1, 10),
        TestResultFilterOptions(status=StatusFilter.FAILED, failure_reason=filter_by),
    )

    assert [x.id for x in result_paginated.entities] == ids


def test_find_by_run_id_paginated_should_find_single_test(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_run_id_with_paging(run.id, PageRequest(1, 10))

    assert results == Page(
        page_number=1, page_size=10, total_entity_count=1, entities=[test_result]
    )


def test_find_by_run_id_paginated_should_find_multiple(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result1 = repository.save(test_result)
    test_result.id = 0
    test_result2 = repository.save(test_result)
    test_result.id = 0
    test_result3 = repository.save(test_result)
    test_result.id = 1

    results = repository.find_by_run_id_with_paging(run.id, PageRequest(1, 10))

    assert results == Page(
        page_number=1,
        page_size=10,
        total_entity_count=4,
        entities=[test_result, test_result1, test_result2, test_result3],
    )


def test_find_by_run_id_paginated_should_find_empty_list(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_by_run_id_with_paging(run.id, PageRequest(1, 10))

    assert results == Page(
        page_number=1, page_size=10, total_entity_count=0, entities=[]
    )


def test_find_by_run_id_paginated_should_return_correct_order(
    sessionmaker_fixture, run, suite_result, order_test_data, test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    for name in order_test_data.wrong_order:
        repository.save(
            test_result_factory(
                test_identifier="{0}/{0}".format(name),
                test_name=name,
                suite_result_id=suite_result.id,
            )
        )

    results = repository.find_by_run_id_with_paging(run.id, PageRequest(1, 10))
    names = list(map(lambda x: x.test_name.lower(), results.entities))

    assert names == order_test_data.correct_order_lowercase


def test_find_execution_status_by_run_ids_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result1 = repository.save(test_result)
    test_result.id = 0
    test_result2 = repository.save(test_result)
    test_result.id = 0
    test_result3 = repository.save(test_result)
    test_result.id = 1

    results = repository.find_execution_status_by_run_ids({run.id})

    assert results == {run.id: {UnifiedTestStatus.NOT_STARTED}}


def test_find_execution_status_by_run_ids_should_find_empty_list(
    sessionmaker_fixture, run
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    results = repository.find_execution_status_by_run_ids({run.id})

    assert results == {}


def test_find_execution_status_by_project_id_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_project_id(run.project_id)

    assert result == {run.id: {UnifiedTestStatus.NOT_STARTED}}


def test_find_execution_status_by_project_id_should_not_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_project_id(42)

    assert result == {}


def test_test_count_by_run_id_should_find_one(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.test_count_by_run_id(run.id) == 1


def test_test_count_by_run_id_should_find_nothing(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.test_count_by_run_id(run.id) == 0


def test_duration_by_run_id_single_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_id(run.id) == test_result.seconds


def test_duration_by_run_id_multiple_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    repository.save(test_result)

    assert repository.duration_by_run_id(run.id) == 10


def test_duration_by_run_id_no_tests(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_id(run.id) == 0


def test_duration_by_run_id_respect_running_tests(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result.unified_test_status = UnifiedTestStatus.RUNNING
    test_result.started_at = datetime.datetime.now() - datetime.timedelta(seconds=10)
    repository.save(test_result)

    assert repository.duration_by_run_id(run.id) == 20


def test_find_execution_status_by_suite_ids(
    sessionmaker_fixture, suite_result, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_suite_ids({suite_result.id})

    assert result == {suite_result.id: {UnifiedTestStatus.NOT_STARTED}}


def test_find_execution_status_by_suite_ids_should_return_empty(
    sessionmaker_fixture, suite_result, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_execution_status_by_suite_ids({42})

    assert result == {}


def test_find_by_run_id_and_test_identifier_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_and_test_identifier(
        run.id, test_result.test_identifier
    )

    assert result == test_result


def test_find_by_run_id_and_test_identifier_should_not_find(
    sessionmaker_fixture, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_and_test_identifier(
        42, test_result.test_identifier
    )

    assert result is None


def test_find_by_run_id_filter_by_test_status_should_not_find_not_existing_run_id(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(
        42, UnifiedTestStatus.SUCCESS
    )

    assert result == []


def test_find_by_run_id_filter_by_test_status_should_not_find_not_matching_status(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(
        run.id, UnifiedTestStatus.FAILED
    )

    assert result == []


def test_find_by_run_id_filter_by_test_status_should_find(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    result = repository.find_by_run_id_filter_by_test_status(
        run.id, UnifiedTestStatus.NOT_STARTED
    )

    assert result == [test_result]


def test_find_by_run_id_filter_by_test_status_should_return_correct_order(
    sessionmaker_fixture, run, suite_result, order_test_data, test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    for name in order_test_data.wrong_order:
        repository.save(
            test_result_factory(
                test_name=name,
                suite_result_id=suite_result.id,
                unified_test_status=UnifiedTestStatus.FAILED,
            )
        )

    results = repository.find_by_run_id_filter_by_test_status(
        run.id, UnifiedTestStatus.FAILED
    )
    names = list(map(lambda x: x.test_name.lower(), results))

    assert names == order_test_data.correct_order_lowercase


def test_duration_by_run_ids(
    sessionmaker_fixture, run, suite_result, test_result, test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    repository.save(
        test_result_factory(
            suite_result_id=suite_result.id,
            unified_test_status=UnifiedTestStatus.RUNNING,
            seconds=0,
            started_at=(datetime.datetime.now() - datetime.timedelta(seconds=5)),
        )
    )
    durations = repository.duration_by_run_ids({run.id})

    assert durations == {1: 10.0}


def test_duration_by_run_ids_single_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_ids({run.id}) == {1: test_result.seconds}


def test_duration_by_run_ids_multiple_test(sessionmaker_fixture, run, test_result):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    repository.save(test_result)

    assert repository.duration_by_run_ids({run.id}) == {1: 10.0}


def test_duration_by_run_ids_no_tests(sessionmaker_fixture, run):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    assert repository.duration_by_run_ids({run.id}) == {1: 0}


def test_duration_by_run_ids_respect_running_tests(
    sessionmaker_fixture, run, test_result
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    test_result.id = 0
    test_result.unified_test_status = UnifiedTestStatus.RUNNING
    test_result.started_at = datetime.datetime.now() - datetime.timedelta(seconds=10)
    repository.save(test_result)

    assert repository.duration_by_run_ids({run.id}) == {1: 20.0}


def test_status_information_by_run_id_empty_for_not_existing_run_id(
    sessionmaker_fixture,
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    status_information = repository.status_information_by_run_id(42)

    assert status_information == TestResultStatusInformation(
        not_started=0, running=0, failed=0, success=0
    )


def test_status_information_by_run_id_empty_run_should_return_all_0(
    sessionmaker_fixture, run
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)

    status_information = repository.status_information_by_run_id(run.id)

    assert status_information == TestResultStatusInformation(
        not_started=0, running=0, failed=0, success=0
    )


def test_status_information_by_run_id_run_with_single_not_started_test(
    sessionmaker_fixture, run, suite_result, saving_test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    saving_test_result_factory(
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
        suite_result_id=suite_result.id,
    )
    status_information = repository.status_information_by_run_id(run.id)

    assert status_information == TestResultStatusInformation(
        not_started=1, running=0, failed=0, success=0
    )


def test_status_information_by_run_id_run_with_single_running_test(
    sessionmaker_fixture, run, suite_result, saving_test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    saving_test_result_factory(
        unified_test_status=UnifiedTestStatus.RUNNING,
        suite_result_id=suite_result.id,
    )
    status_information = repository.status_information_by_run_id(run.id)

    assert status_information == TestResultStatusInformation(
        not_started=0, running=1, failed=0, success=0
    )


def test_status_information_by_run_id_run_with_single_failed_test(
    sessionmaker_fixture, run, suite_result, saving_test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    saving_test_result_factory(
        unified_test_status=UnifiedTestStatus.FAILED,
        suite_result_id=suite_result.id,
    )
    status_information = repository.status_information_by_run_id(run.id)

    assert status_information == TestResultStatusInformation(
        not_started=0, running=0, failed=1, success=0
    )


def test_status_information_by_run_id_run_with_single_succeded_test(
    sessionmaker_fixture, run, suite_result, saving_test_result_factory
):
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    saving_test_result_factory(
        unified_test_status=UnifiedTestStatus.SUCCESS,
        suite_result_id=suite_result.id,
    )
    status_information = repository.status_information_by_run_id(run.id)

    assert status_information == TestResultStatusInformation(
        not_started=0, running=0, failed=0, success=1
    )


def test_status_information_by_run_id_multiple_runs_only_correct_run(
    sessionmaker_fixture,
    suite_result,
    saving_test_result_factory,
    saving_run_factory,
    saving_suite_result_factory,
):
    run_1 = saving_run_factory()
    run_2 = saving_run_factory()
    suite_result_1 = saving_suite_result_factory(run_id=run_1.id)
    suite_result_2 = saving_suite_result_factory(run_id=run_2.id)
    test_result_run_1_1 = saving_test_result_factory(
        suite_result_id=suite_result_1.id,
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
    )
    test_result_run_1_2 = saving_test_result_factory(
        suite_result_id=suite_result_1.id,
        unified_test_status=UnifiedTestStatus.RUNNING,
    )
    test_result_run_1_3 = saving_test_result_factory(
        suite_result_id=suite_result_1.id,
        unified_test_status=UnifiedTestStatus.SUCCESS,
    )
    test_result_run_1_5 = saving_test_result_factory(
        suite_result_id=suite_result_1.id,
        unified_test_status=UnifiedTestStatus.FAILED,
    )
    test_result_run_1_1 = saving_test_result_factory(
        suite_result_id=suite_result_2.id,
        unified_test_status=UnifiedTestStatus.NOT_STARTED,
    )
    test_result_run_1_2 = saving_test_result_factory(
        suite_result_id=suite_result_2.id,
        unified_test_status=ExecutionStatus.RUNNING,
    )
    repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    saving_test_result_factory(
        unified_test_status=UnifiedTestStatus.SUCCESS,
        suite_result_id=suite_result.id,
    )

    status_information_run_1 = repository.status_information_by_run_id(run_1.id)
    assert status_information_run_1 == TestResultStatusInformation(
        not_started=1, running=1, failed=1, success=1
    )

    status_information_run_2 = repository.status_information_by_run_id(run_2.id)
    assert status_information_run_2 == TestResultStatusInformation(
        not_started=1, running=1, failed=0, success=0
    )
