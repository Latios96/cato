import pytest

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry
from cato.utils.machine_info_cache import MachineInfoCache
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_common.config.user_local_storage.user_local_storage import UserLocalStorage
from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from tests.utils import mock_safe


@pytest.fixture
def test_context():
    class TestContext:
        def __init__(self):
            self.mock_user_local_storage_repository = mock_safe(
                UserLocalStorageRepository
            )
            self.mock_machine_info_collector = mock_safe(MachineInfoCollector)
            self.machine_info_cache = MachineInfoCache(
                self.mock_user_local_storage_repository,
                self.mock_machine_info_collector,
            )

    return TestContext()


class TestUseFromUserLocalStorage:
    def test_no_cached_value_should_use_user_local_storage(
        self, test_context, machine_info
    ):
        test_context.mock_user_local_storage_repository.read.return_value = (
            UserLocalStorage(
                machine_info_cache_entry=MachineInfoCacheEntry(machine_info)
            )
        )

        cached_machine_info = test_context.machine_info_cache.get_machine_info()

        assert cached_machine_info == machine_info
        test_context.mock_user_local_storage_repository.read.assert_called_once()
        test_context.mock_machine_info_collector.collect.assert_not_called()

    def test_collect_should_cache_value(self, test_context, machine_info):
        test_context.mock_user_local_storage_repository.read.return_value = (
            UserLocalStorage(
                machine_info_cache_entry=MachineInfoCacheEntry(machine_info)
            )
        )

        cached_machine_info_1 = test_context.machine_info_cache.get_machine_info()
        cached_machine_info_2 = test_context.machine_info_cache.get_machine_info()

        assert cached_machine_info_1 is cached_machine_info_2
        test_context.mock_user_local_storage_repository.read.assert_called_once()
        test_context.mock_machine_info_collector.collect.assert_not_called()


class TestCollect:
    def test_no_value_should_collect_machine_info(self, test_context, machine_info):
        test_context.mock_user_local_storage_repository.read.return_value = (
            UserLocalStorage()
        )
        test_context.mock_machine_info_collector.collect.return_value = machine_info

        cached_machine_info = test_context.machine_info_cache.get_machine_info()

        assert cached_machine_info == machine_info
        test_context.mock_user_local_storage_repository.read.assert_called_once()
        test_context.mock_machine_info_collector.collect.assert_called_once()

    def test_collect_should_cache_value(self, test_context, machine_info):
        test_context.mock_user_local_storage_repository.read.return_value = (
            UserLocalStorage()
        )
        test_context.mock_machine_info_collector.collect.return_value = machine_info

        cached_machine_info_1 = test_context.machine_info_cache.get_machine_info()
        cached_machine_info_2 = test_context.machine_info_cache.get_machine_info()

        assert cached_machine_info_1 is cached_machine_info_2
        test_context.mock_user_local_storage_repository.read.assert_called_once()
        test_context.mock_machine_info_collector.collect.assert_called_once()
