import datetime
import logging

from flask import Blueprint, jsonify

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.mappers.test_heartbeat_dto_class_mapper import (
    TestHeartbeatDtoClassMapper,
)
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.abstract.test_result_repository import TestResultRepository

from cato_api_models.catoapimodels import TestHeartbeatDto

logger = logging.getLogger(__name__)


class TestHeartbeatBlueprint(Blueprint):
    def __init__(
        self,
        test_result_repository: TestResultRepository,
        test_heartbeat_repository: TestHeartbeatRepository,
    ):
        super(TestHeartbeatBlueprint, self).__init__("test_heartbeats", __name__)

        self._test_result_repository = test_result_repository
        self._test_heartbeat_repository = test_heartbeat_repository

        self._test_heartbeat_dto_class_mapper = TestHeartbeatDtoClassMapper()

        self.route("/test_heartbeats/<int:test_result_id>", methods=["POST"])(
            self.register_heartbeat
        )

    def register_heartbeat(self, test_result_id):
        if not self._test_result_repository.find_by_id(test_result_id):
            return (
                jsonify(
                    {"test_result_id": f"No test result found with id {test_result_id}"}
                ),
                400,
            )

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
                test_result_id,
                beat_time,
            )
            test_heartbeat.last_beat = beat_time
        test_heartbeat = self._test_heartbeat_repository.save(test_heartbeat)
        test_heartbeat_dto = TestHeartbeatDto(
            id=test_heartbeat.id,
            test_result_id=test_heartbeat.test_result_id,
            last_beat=test_heartbeat.last_beat.isoformat(),
        )
        return jsonify(
            self._test_heartbeat_dto_class_mapper.map_to_dict(test_heartbeat_dto)
        )