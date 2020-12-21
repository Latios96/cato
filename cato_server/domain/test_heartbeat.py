import datetime
from dataclasses import dataclass


@dataclass
class TestHeartbeat:
    id: int
    test_result_id: int
    last_beat: datetime.datetime
