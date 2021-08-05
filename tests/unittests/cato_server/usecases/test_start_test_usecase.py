import datetime

import pytest

from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.event import Event
from cato_server.domain.execution_status import ExecutionStatus
from cato_common.domain.machine_info import MachineInfo
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_server.mappers.object_mapper import ObjectMapper
from cato_server.queues.abstract_message_queue import AbstractMessageQueue
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_server.usecases.start_test import StartTest
from tests.utils import mock_safe
from cato_api_models.catoapimodels import TestResultStartedDto


class TestStartTest:
    def setup_method(self, method):
        self.test_result_repository = mock_safe(TestResultRepository)
        self.message_queue = OptionalComponent(mock_safe(AbstractMessageQueue))
        self.object_mapper = ObjectMapper(
            MapperRegistryFactory().create_mapper_registry()
        )
        self.machine_info = MachineInfo("cpu_name", 1, 1)
        self.start_test_usecase = StartTest(
            self.test_result_repository,
            self.message_queue,
            self.object_mapper,
        )

    def test_starting_a_not_existing_test_should_fail(self):
        self.test_result_repository.find_by_id.return_value = None

        with pytest.raises(ValueError):
            self.start_test_usecase.start_test(42, MachineInfo("cpu_name", 1, 1))

        self.test_result_repository.save.assert_not_called()

    def test_starting_an_existing_test_should_set_status_and_start_time(
        self, test_result_factory
    ):
        test_result = test_result_factory()
        test_result.started_at = None
        test_result.execution_status = ExecutionStatus.NOT_STARTED
        self.test_result_repository.find_by_id.return_value = test_result
        self.test_result_repository.save.return_value = test_result
        event_dto = TestResultStartedDto(test_result.id)
        event = Event("TEST_RESULT_STARTED", event_dto)

        self.start_test_usecase.start_test(1, MachineInfo("cpu_name", 1, 1))

        self.test_result_repository.save.assert_called_with(test_result)
        assert test_result.execution_status == ExecutionStatus.RUNNING
        assert test_result.started_at is not None
        assert test_result.machine_info == self.machine_info
        self.message_queue.component.send_event.assert_called_with(
            "test_result_events",
            str(test_result.suite_result_id),
            event,
            self.object_mapper,
        )

    def test_starting_an_existing_which_was_started_at_least_once_should_reset_data(
        self, test_result_factory
    ):
        test_result = test_result_factory()
        test_result.started_at = datetime.datetime.now()
        test_result.execution_status = ExecutionStatus.RUNNING
        self.test_result_repository.find_by_id.return_value = test_result
        assert test_result.machine_info != self.machine_info

        self.start_test_usecase.start_test(1, self.machine_info)

        self.test_result_repository.save.assert_called_with(test_result)
        self.message_queue.component.send_event.assert_called_once()
        assert test_result.execution_status == ExecutionStatus.RUNNING
        assert test_result.started_at is not None
        assert test_result.status == None
        assert test_result.seconds == None
        assert test_result.message == None
        assert test_result.image_output == None
        assert test_result.reference_image == None
        assert test_result.finished_at == None
        assert test_result.machine_info == self.machine_info
