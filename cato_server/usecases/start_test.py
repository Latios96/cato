import datetime
import logging

from cato_server.configuration.optional_component import OptionalComponent
from cato_server.domain.event import Event
from cato_common.domain.execution_status import ExecutionStatus
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_result import TestResult
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_result_repository import TestResultRepository
from cato_api_models.catoapimodels import TestResultStartedDto


logger = logging.getLogger(__name__)


class StartTest:
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        object_mapper: ObjectMapper,
    ):
        self._test_result_repository = test_result_repository
        self._object_mapper = object_mapper

    def start_test(self, test_result_id: int, machine_info: MachineInfo) -> None:
        logger.info("Starting test test with id %s", test_result_id)
        test_result = self._test_result_repository.find_by_id(test_result_id)
        if not test_result:
            raise ValueError(f"No TestResult with id {test_result_id} found!")

        test_was_already_started = (
            test_result.execution_status != ExecutionStatus.NOT_STARTED
        )

        test_result.execution_status = ExecutionStatus.RUNNING
        test_result.started_at = datetime.datetime.now()
        test_result.machine_info = machine_info

        if test_was_already_started:
            self._reset_possible_data_from_previous_run(test_result)

        test_result = self._test_result_repository.save(test_result)
        logger.info("Started test %s", test_result)

    def _reset_possible_data_from_previous_run(self, test_result: TestResult) -> None:
        logger.info(
            "Reseting data from previos run for test with id %s", test_result.id
        )
        test_result.status = None
        test_result.seconds = None
        test_result.message = None
        test_result.image_output = None
        test_result.reference_image = None
        test_result.finished_at = None
