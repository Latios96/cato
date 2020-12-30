from cato_server.domain.machine_info import MachineInfo
from cato_server.mappers.internal.machine_info_class_mapper import (
    MachineInfoClassMapper,
)


def test_map_from_dict():
    data = {"cpu_name": "Intel Xeon", "cores": 8, "memory": 2}
    mapper = MachineInfoClassMapper()

    result = mapper.map_from_dict(data)

    assert result == MachineInfo("Intel Xeon", 8, 2)


def test_map_to_dict():
    mapper = MachineInfoClassMapper()

    result = mapper.map_to_dict(MachineInfo("Intel Xeon", 8, 2))

    assert result == {"cpu_name": "Intel Xeon", "cores": 8, "memory": 2}
