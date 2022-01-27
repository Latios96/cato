import os
from typing import Optional

from cato_server.backup.backup_creator import BackupCreator
from cato_server.backup.backup_mode import BackupMode
from cato_server.backup.create_db_backup import CreateDbBackup
from cato_server.backup.create_file_storage_backup import CreateFileStorageBackup
from cato_server.backup.pg_dump_path_resolver import PgDumpPathResolver
from cato_server.configuration.app_configuration_reader import AppConfigurationReader


class CreateBackupCommand:
    def create_backup(
        self, path: str, pg_dump_executable: Optional[str], mode_str: Optional[str]
    ) -> None:
        app_config = AppConfigurationReader().read_file(path)

        pg_dump_path_resolver = PgDumpPathResolver()
        pg_dump_path = pg_dump_path_resolver.resolve(pg_dump_executable)

        create_file_storage_backup = CreateFileStorageBackup(
            app_config.storage_configuration
        )
        create_db_backup = CreateDbBackup(
            app_config.storage_configuration, pg_dump_path
        )

        mode = BackupMode(mode_str) if mode_str else BackupMode.FULL

        backup_creator = BackupCreator(create_file_storage_backup, create_db_backup)
        backup_creator.create_backup(os.getcwd(), mode)
