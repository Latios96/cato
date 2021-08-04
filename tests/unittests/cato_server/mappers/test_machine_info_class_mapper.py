from cato_server.domain.machine_info import MachineInfo


def test_map_from_dict(object_mapper):
    data = {"cpu_name": "Intel Xeon", "cores": 8, "memory": 2}

    result = object_mapper.from_dict(data, MachineInfo)

    assert result == MachineInfo("Intel Xeon", 8, 2)


def test_map_to_dict(object_mapper):
    result = object_mapper.to_dict(MachineInfo("Intel Xeon", 8, 2))

    assert result == {"cpu_name": "Intel Xeon", "cores": 8, "memory": 2}
