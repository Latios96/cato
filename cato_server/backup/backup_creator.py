import datetime
import os.path
import tarfile
import tempfile
import time

import humanfriendly

from cato_server.backup.create_db_backup import CreateDbBackup
from cato_server.backup.create_file_storage_backup import CreateFileStorageBackup

import logging

logger = logging.getLogger(__name__)


class BackupCreator:
    def __init__(
        self,
        create_file_storage_backup: CreateFileStorageBackup,
        create_db_backup: CreateDbBackup,
    ):
        self._create_file_storage_backup = create_file_storage_backup
        self._create_db_backup = create_db_backup

    def create_backup(self, folder: str) -> str:
        start = time.time()
        if not os.path.isdir(folder):
            raise ValueError(f"The provided path {folder} is not a folder!")

        now = datetime.datetime.now().strftime("%m-%d-%Y-%H-%M-%S")

        logger.info("Creating cato backup..")

        with tempfile.TemporaryDirectory() as tmpdirname:
            cato_backup_path = self._create_individual_parts_of_the_backup(
                folder, now, tmpdirname
            )

        stop = time.time()
        logger.info("Successfully created cato backup at %s", cato_backup_path)
        logger.info(
            "Backup creation took %s", humanfriendly.format_timespan(stop - start)
        )

        return cato_backup_path

    def _create_individual_parts_of_the_backup(self, folder, now, tmpdirname):
        file_storage_backup_path = os.path.join(
            tmpdirname, f"cato-backup-filestorage-{now}.tar"
        )
        db_backup_path = os.path.join(tmpdirname, f"cato-backup-filestorage-{now}.sql")
        cato_backup_path = os.path.join(folder, f"cato-backup-full-{now}.tar.gz")

        self._create_file_storage_backup.create_backup(file_storage_backup_path)
        self._create_db_backup.create_backup(db_backup_path)

        self._combine_backup_parts(
            cato_backup_path, db_backup_path, file_storage_backup_path
        )
        return cato_backup_path

    def _combine_backup_parts(
        self, cato_backup_path, db_backup_path, file_storage_backup_path
    ):
        logger.info("Creating compressed cato backup archive..")
        with tarfile.open(cato_backup_path, "w:gz") as tar:
            tar.add(
                file_storage_backup_path,
                arcname=os.path.basename(file_storage_backup_path),
            )
            tar.add(db_backup_path, arcname=os.path.basename(db_backup_path))
