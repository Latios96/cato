from typing import Optional

import cpuinfo
import psutil

from cato_common.domain.machine_info import MachineInfo


class MachineInfoCollector:
    def __init__(self):
        self._cached: Optional[MachineInfo] = None

    def collect(self) -> MachineInfo:
        if not self._cached:
            cpu_info = cpuinfo.get_cpu_info()
            memory = psutil.virtual_memory().total
            self._cached = MachineInfo(
                cpu_name=cpu_info["brand_raw"],
                cores=cpu_info["count"],
                memory=memory,
            )

        return self._cached
