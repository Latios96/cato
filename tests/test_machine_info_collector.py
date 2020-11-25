from cato.utils.machine_info_collector import MachineInfoCollector


def test_collect():
    machine_info_collector = MachineInfoCollector()

    result = machine_info_collector.collect()

    assert result.cpu_name
    assert result.memory
    assert result.cores
    assert result.memory_str.endswith("GB")
