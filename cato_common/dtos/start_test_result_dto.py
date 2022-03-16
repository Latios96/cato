from dataclasses import dataclass

from cato_common.domain.machine_info import MachineInfo


@dataclass
class StartTestResultDto:
    id: int
    machine_info: MachineInfo
