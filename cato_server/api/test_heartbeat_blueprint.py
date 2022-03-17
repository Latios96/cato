import datetime
import logging

from fastapi import APIRouter
from starlette.responses import JSONResponse, Response

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.mappers.object_mapper import ObjectMapper
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository

logger = logging.getLogger(__name__)


class TestHeartbeatBlueprint(APIRouter):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
        object_mapper: ObjectMapper,
    ):
        super(TestHeartbeatBlueprint, self).__init__()

        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository

        self._object_mapper = object_mapper

        self.post("/test_heartbeats/{test_result_id}")(self.register_heartbeat)
        self.post(
            "/test_heartbeats/run/{run_id}/{suite_name}/{test_name}",
        )(self.register_heartbeat_by_run_id)

    def register_heartbeat(self, test_result_id: int) -> Response:
        if not self._test_result_repository.find_by_id(test_result_id):
            return JSONResponse(
                content={
                    "testResultId": f"No test result found with id {test_result_id}"
                },
                status_code=400,
            )

        return self._handle_heartbeat_registration(test_result_id)

    def register_heartbeat_by_run_id(
        self, run_id: int, suite_name: str, test_name: str
    ) -> Response:
        test_identifier = TestIdentifier(suite_name, test_name)
        test_result = self._test_result_repository.find_by_run_id_and_test_identifier(
            run_id, test_identifier
        )
        if not test_result:
            return JSONResponse(
                content={
                    "runId": f"No test result found with run id {run_id} and test identifier {test_identifier}",
                    "testIdentifier": f"No test result found with run id {run_id} and test identifier {test_identifier}",
                },
                status_code=400,
            )

        return self._handle_heartbeat_registration(test_result.id)

    def _handle_heartbeat_registration(self, test_result_id: int) -> Response:
        test_heartbeat = self._test_heartbeat_repository.find_by_test_result_id(
            test_result_id
        )
        beat_time = datetime.datetime.now()
        if not test_heartbeat:
            logger.info(
                "Creating a new heartbeat at %s for test result with id %s",
                beat_time,
                test_result_id,
            )
            test_heartbeat = TestHeartbeat(
                id=0, test_result_id=test_result_id, last_beat=beat_time
            )
        else:
            logger.info(
                "Updating existing heartbeat with id %s to %s for test result with id %s",
                test_heartbeat.id,
                beat_time,
                test_result_id,
            )
            test_heartbeat.last_beat = beat_time
        test_heartbeat = self._test_heartbeat_repository.save(test_heartbeat)

        return JSONResponse(self._object_mapper.to_dict(test_heartbeat))
