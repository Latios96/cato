import datetime
from typing import Iterable

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class TestHeartbeatRepository(AbstractRepository[TestHeartbeat, int]):
    def find_last_beat_older_than(
        self, date: datetime.datetime
    ) -> Iterable[TestHeartbeat]:
        raise NotImplementedError()
