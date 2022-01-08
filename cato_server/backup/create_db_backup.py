import os
import subprocess

from sqlalchemy.engine import make_url, URL

from cato_server.configuration.storage_configuration import StorageConfiguration

import logging

logger = logging.getLogger(__name__)


class CreateDbBackup:
    def __init__(self, storage_configuration: StorageConfiguration, pg_dump_path: str):
        self._storage_configuration = storage_configuration
        self._pg_dump_path = pg_dump_path

    def create_backup(self, backup_archive_path: str) -> None:
        sqlalchemy_url = make_url(self._storage_configuration.database_url)
        command = self._create_pg_dump_command(backup_archive_path, sqlalchemy_url)

        logger.info("Using %s executable", self._pg_dump_path)
        logger.info("Creating db backup..")
        logger.debug("Running command %s", command)

        completed_process = subprocess.run(
            command,
            stderr=subprocess.STDOUT,
            env=(self._get_env_with_password(sqlalchemy_url)),
        )

        if completed_process.returncode:
            raise Exception(
                f"Exit code {completed_process.returncode} when running command {command}: output was: {completed_process.stdout}"
            )

    def _create_pg_dump_command(
        self, backup_archive_path: str, sqlalchemy_url: URL
    ) -> str:
        return f'"{self._pg_dump_path}" --no-password --file={backup_archive_path} --dbname={sqlalchemy_url.database} --username={sqlalchemy_url.username} --host={sqlalchemy_url.host} --port={sqlalchemy_url.port}'

    def _get_env_with_password(self, url_information):
        env = os.environ.copy()
        env["PGPASSWORD"] = url_information.password
        return env
