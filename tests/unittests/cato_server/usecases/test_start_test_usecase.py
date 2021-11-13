import datetime

import pytest

from cato_api_models.catoapimodels import TestResultStartedDto
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.domain.event import Event
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.start_test import StartTest
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.test_result_repository = mock_safe(TestResultRepository)
            self.object_mapper = ObjectMapper(
                MapperRegistryFactory().create_mapper_registry()
            )
            self.machine_info = MachineInfo("cpu_name", 1, 1)
            self.start_test_usecase = StartTest(
                self.test_result_repository,
                self.object_mapper,
            )

    return TestContext()


class TestStartTest:
    def test_starting_a_not_existing_test_should_fail(self, test_context):
        test_context.test_result_repository.find_by_id.return_value = None

        with pytest.raises(ValueError):
            test_context.start_test_usecase.start_test(
                42, MachineInfo("cpu_name", 1, 1)
            )

        test_context.test_result_repository.save.assert_not_called()

    def test_starting_an_existing_test_should_set_status_and_start_time(
        self, test_result_factory, test_context
    ):
        test_result = test_result_factory()
        test_result.started_at = None
        test_result.unified_test_status = UnifiedTestStatus.NOT_STARTED
        test_context.test_result_repository.find_by_id.return_value = test_result
        test_context.test_result_repository.save.return_value = test_result
        event_dto = TestResultStartedDto(test_result.id)
        event = Event("TEST_RESULT_STARTED", event_dto)

        test_context.start_test_usecase.start_test(1, MachineInfo("cpu_name", 1, 1))

        test_context.test_result_repository.save.assert_called_with(test_result)
        assert test_result.unified_test_status == UnifiedTestStatus.RUNNING
        assert test_result.started_at is not None
        assert test_result.machine_info == test_context.machine_info

    def test_starting_an_existing_which_was_started_at_least_once_should_reset_data(
        self, test_result_factory, test_context
    ):
        test_result = test_result_factory(
            started_at=datetime.datetime.now(),
            unified_test_status=UnifiedTestStatus.FAILED,
            failure_reason=TestFailureReason.EXIT_CODE_NON_ZERO,
        )
        test_context.test_result_repository.find_by_id.return_value = test_result
        assert test_result.machine_info != test_context.machine_info

        test_context.start_test_usecase.start_test(1, test_context.machine_info)

        test_context.test_result_repository.save.assert_called_with(test_result)
        assert test_result.unified_test_status == ExecutionStatus.RUNNING
        assert test_result.started_at is not None
        assert test_result.seconds is None
        assert test_result.message is None
        assert test_result.image_output is None
        assert test_result.reference_image is None
        assert test_result.finished_at is None
        assert test_result.machine_info == test_context.machine_info
        assert test_result.failure_reason is None
