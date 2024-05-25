import datetime
from dataclasses import dataclass, field

from cato_common.domain.machine_info import MachineInfo
from cato_common.utils.datetime_utils import aware_now_in_utc


@dataclass
class MachineInfoCacheEntry:
    machine_info: MachineInfo
    timestamp: datetime.datetime = field(default_factory=aware_now_in_utc)

    def is_valid(self) -> bool:
        now = aware_now_in_utc()
        age = now - self.timestamp
        seconds_per_day = 24 * 60 * 60
        is_expired = age.total_seconds() <= seconds_per_day
        return is_expired
