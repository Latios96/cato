import datetime
from dataclasses import dataclass


@dataclass
class TestHeartbeat:
    __test__ = False

    id: int
    test_result_id: int
    last_beat: datetime.datetime
