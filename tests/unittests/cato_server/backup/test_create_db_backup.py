import os.path
from subprocess import CompletedProcess
from unittest import mock

import pytest

from cato_server.backup.create_db_backup import CreateDbBackup
from cato_server.configuration.storage_configuration import StorageConfiguration


@pytest.fixture
def create_db_backup_setup():
    storage_configuration = StorageConfiguration(
        file_storage_url="file_storage_url",
        database_url="postgresql+psycopg2://postgres:postgres@localhost:5432/cato-example",
    )
    create_db_backup = CreateDbBackup(storage_configuration, "pg_dump")
    with mock.patch("subprocess.run") as mock_subprocess_run:
        yield create_db_backup, mock_subprocess_run


def test_should_call_pg_dump_correctly(create_db_backup_setup, tmp_path):
    create_db_backup, mock_subprocess_run = create_db_backup_setup
    db_backup_path = str(tmp_path / "backup.sql")
    mock_subprocess_run.return_value = CompletedProcess([], 0)

    create_db_backup.create_backup(db_backup_path)

    mock_subprocess_run.assert_called_once()
    assert mock_subprocess_run.call_args[0] == (
        f'"pg_dump" --no-password --file={db_backup_path} --dbname=cato-example --username=postgres --host=localhost --port=5432',
    )
    assert mock_subprocess_run.call_args[1]["env"]["PGPASSWORD"] == "postgres"


def test_should_raise_exception_if_pg_dump_failed(create_db_backup_setup, tmp_path):
    create_db_backup, mock_subprocess_run = create_db_backup_setup
    db_backup_path = str(tmp_path / "backup.sql")
    mock_subprocess_run.return_value = CompletedProcess([], 1)

    with pytest.raises(Exception):
        create_db_backup.create_backup(db_backup_path)

    mock_subprocess_run.assert_called_once()
    assert mock_subprocess_run.call_args[0] == (
        f'"pg_dump" --no-password --file={db_backup_path} --dbname=cato-example --username=postgres --host=localhost --port=5432',
    )
    assert mock_subprocess_run.call_args[1]["env"]["PGPASSWORD"] == "postgres"
