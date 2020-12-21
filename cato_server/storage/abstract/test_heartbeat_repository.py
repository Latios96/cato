import datetime
from typing import Iterable, Optional

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class TestHeartbeatRepository(AbstractRepository[TestHeartbeat, int]):
    def find_by_test_result_id(self, test_result_id) -> Optional[TestHeartbeat]:
        raise NotImplementedError()

    def find_last_beat_older_than(
        self, date: datetime.datetime
    ) -> Iterable[TestHeartbeat]:
        raise NotImplementedError()
