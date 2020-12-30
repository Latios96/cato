from typing import Dict

from cato_server.domain.machine_info import MachineInfo
from cato_server.mappers.abstract_class_mapper import AbstractClassMapper


class MachineInfoClassMapper(AbstractClassMapper[MachineInfo]):
    def map_from_dict(self, the_dict: Dict) -> MachineInfo:
        return MachineInfo(
            cpu_name=the_dict["cpu_name"],
            cores=the_dict["cores"],
            memory=the_dict["memory"],
        )

    def map_to_dict(self, machine_info: MachineInfo) -> Dict:
        return {
            "cpu_name": machine_info.cpu_name,
            "cores": machine_info.cores,
            "memory": machine_info.memory,
        }
