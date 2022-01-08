import subprocess

from cato_server.configuration.storage_configuration import StorageConfiguration

import logging

logger = logging.getLogger(__name__)


class CreateFileStorageBackup:
    def __init__(self, storage_configuration: StorageConfiguration):
        self._storage_configuration = storage_configuration

    def create_backup(self, backup_archive_path: str) -> None:
        command = f"tar -cf {backup_archive_path} {self._storage_configuration.file_storage_url}"

        logger.info("Creating file storage backup..")
        logger.debug("Running command %s", command)

        completed_process = subprocess.run(command)
        if completed_process.returncode:
            raise Exception(
                f"Exit code {completed_process.returncode} when running command {command}: output was: {completed_process.stdout}"
            )
