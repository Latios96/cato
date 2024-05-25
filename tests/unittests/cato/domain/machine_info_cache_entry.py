import datetime

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry


class TestMachineInfoCacheEntryIsValid:

    def test_is_valid_fresh_created(self, machine_info):
        machine_info_cache_entry = MachineInfoCacheEntry(machine_info)

        assert machine_info_cache_entry.is_valid()

    def test_is_invalid(self, machine_info):
        machine_info_cache_entry = MachineInfoCacheEntry(
            machine_info,
            timestamp=datetime.datetime(2020, 1, 1, tzinfo=datetime.timezone.utc),
        )

        assert not machine_info_cache_entry.is_valid()
