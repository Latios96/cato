import datetime
from typing import Optional, List

from cato_common.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class TestHeartbeatRepository(AbstractRepository[TestHeartbeat, int]):
    __test__ = False

    def find_by_test_result_id(self, test_result_id: int) -> Optional[TestHeartbeat]:
        raise NotImplementedError()

    def find_last_beat_older_than(self, date: datetime.datetime) -> List[TestHeartbeat]:
        raise NotImplementedError()
