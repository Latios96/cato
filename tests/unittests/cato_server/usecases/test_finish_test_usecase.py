import datetime

import pytest

from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_status import TestStatus
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.create_thumbnail import CreateThumbnail
from cato_server.usecases.finish_test import FinishTest
from tests.utils import mock_safe


def test_should_finish(test_result_factory, object_mapper):
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.save.side_effect = lambda x: x
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=42, started_at=started_at
    )
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    mock_create_thumbnail = mock_safe(CreateThumbnail)
    finish_test = FinishTest(
        test_result_repository,
        test_heartbeat_repository,
        object_mapper,
        mock_create_thumbnail,
    )
    finish_test._get_finished_time = lambda: finished_at

    finish_test.finish_test(
        test_result_id=42,
        status=TestStatus.SUCCESS,
        seconds=2,
        message="Test succeded",
        image_output=2,
        reference_image=3,
        diff_image=4,
        error_value=1,
    )

    expected_test_result = test_result_factory(
        id=42,
        unified_test_status=UnifiedTestStatus.SUCCESS,
        seconds=2,
        message="Test succeded",
        image_output=2,
        reference_image=3,
        diff_image=4,
        started_at=started_at,
        finished_at=finished_at,
        error_value=1,
        failure_reason=None,
    )
    test_result_repository.save.assert_called_with(expected_test_result)
    test_heartbeat_repository.delete_by_id.assert_called_with(2)
    mock_create_thumbnail.create_thumbnail.assert_called_with(expected_test_result)


def test_should_raise_no_test_result_with_id(object_mapper):
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.find_by_id.return_value = None
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    mock_create_thumbnail = mock_safe(CreateThumbnail)
    finish_test = FinishTest(
        test_result_repository,
        test_heartbeat_repository,
        object_mapper,
        mock_create_thumbnail,
    )

    with pytest.raises(ValueError):
        finish_test.finish_test(
            test_result_id=42,
            status=TestStatus.SUCCESS,
            seconds=2,
            message="Test succeded",
            image_output=2,
            reference_image=3,
            diff_image=4,
        )


def test_should_fail_test(test_result_factory, object_mapper):
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.save.side_effect = lambda x: x
    started_at = datetime.datetime.now()
    finished_at = datetime.datetime.now()
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=42, started_at=started_at
    )
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    test_heartbeat_repository.find_by_test_result_id.return_value = TestHeartbeat(
        id=2, test_result_id=42, last_beat=datetime.datetime.now()
    )
    mock_create_thumbnail = mock_safe(CreateThumbnail)
    finish_test = FinishTest(
        test_result_repository,
        test_heartbeat_repository,
        object_mapper,
        mock_create_thumbnail,
    )
    finish_test._get_finished_time = lambda: finished_at

    finish_test.fail_test(42, "This is a test", TestFailureReason.EXIT_CODE_NON_ZERO)

    test_result_repository.save.assert_called_with(
        test_result_factory(
            id=42,
            unified_test_status=UnifiedTestStatus.FAILED,
            seconds=-1,
            message="This is a test",
            image_output=None,
            reference_image=None,
            diff_image=None,
            started_at=started_at,
            finished_at=finished_at,
            error_value=None,
            failure_reason=TestFailureReason.EXIT_CODE_NON_ZERO,
        )
    )
    test_heartbeat_repository.delete_by_id.assert_called_with(2)
    mock_create_thumbnail.create_thumbnail.assert_not_called()


def test_exception_during_thumbnail_creation_should_not_be_an_issue(
    test_result_factory, object_mapper
):
    test_result_repository = mock_safe(TestResultRepository)
    test_result_repository.save.side_effect = lambda x: x
    test_result_repository.find_by_id.return_value = test_result_factory(
        id=42, started_at=(datetime.datetime.now())
    )
    test_heartbeat_repository = mock_safe(TestHeartbeatRepository)
    mock_create_thumbnail = mock_safe(CreateThumbnail)
    mock_create_thumbnail.create_thumbnail.side_effect = Exception()
    finish_test = FinishTest(
        test_result_repository,
        test_heartbeat_repository,
        object_mapper,
        mock_create_thumbnail,
    )
    finish_test.finish_test(
        test_result_id=42,
        status=TestStatus.SUCCESS,
        seconds=2,
        message="Test succeded",
        image_output=2,
        reference_image=3,
        diff_image=4,
        error_value=1,
    )

    test_result_repository.save.assert_called_once()
    mock_create_thumbnail.create_thumbnail.assert_called_once()
