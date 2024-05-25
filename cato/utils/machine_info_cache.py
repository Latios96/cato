from typing import Optional

from cato.domain.machine_info_cache_entry import MachineInfoCacheEntry
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_common.config.user_local_storage.user_local_storage_repository import (
    UserLocalStorageRepository,
)
from cato_common.domain.machine_info import MachineInfo

import logging

logger = logging.getLogger(__name__)


class MachineInfoCache(object):
    def __init__(
        self,
        user_local_storage_repository: UserLocalStorageRepository,
        machine_info_collector: MachineInfoCollector,
    ):
        self._user_local_storage_repository = user_local_storage_repository
        self._machine_info_collector = machine_info_collector
        self._cached: Optional[MachineInfo] = None

    def get_machine_info(self):
        if self._cached:
            return self._cached

        user_local_storage = self._user_local_storage_repository.read()
        machine_info_cache_entry = user_local_storage.machine_info_cache_entry

        if machine_info_cache_entry is not None and machine_info_cache_entry.is_valid():
            self._cached = machine_info_cache_entry.machine_info
            logger.info("Using cached MachineInfo")
            return self._cached

        logger.info("Collecting MachineInfo (once per day)..")
        machine_info = self._machine_info_collector.collect()
        user_local_storage.machine_info_cache_entry = MachineInfoCacheEntry(
            machine_info=machine_info
        )
        self._user_local_storage_repository.write(user_local_storage)
        self._cached = machine_info
        return self._cached
