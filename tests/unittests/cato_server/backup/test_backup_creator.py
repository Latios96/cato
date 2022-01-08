import datetime
import os.path
import uuid
from pathlib import Path

import pytest
from freezegun import freeze_time

from cato_server.backup.backup_creator import BackupCreator
from cato_server.backup.create_db_backup import CreateDbBackup
from cato_server.backup.create_file_storage_backup import CreateFileStorageBackup
from tests.utils import mock_safe


@freeze_time(datetime.datetime(2022, 8, 1))
def test_should_create_backup_with_success(tmp_path):
    mock_create_file_storage_backup = mock_safe(CreateFileStorageBackup)
    mock_create_file_storage_backup.create_backup.side_effect = lambda x: Path(
        x
    ).touch()
    mock_create_db_backup = mock_safe(CreateDbBackup)
    mock_create_db_backup.create_backup.side_effect = lambda x: Path(x).touch()
    backup_creator = BackupCreator(
        mock_create_file_storage_backup, mock_create_db_backup
    )

    cato_backup_path = backup_creator.create_backup(str(tmp_path))

    assert os.path.exists(cato_backup_path)
    mock_create_file_storage_backup.create_backup.call_args[0][0].endswith(
        "cato-backup-filestorage-08-01-2022-00-00-00.tar"
    )
    mock_create_db_backup.create_backup.call_args[0][0].endswith(
        "cato-backup-db-08-01-2022-00-00-00.tar"
    )


def test_should_fail_if_provided_path_does_not_exist(tmp_path):
    mock_create_file_storage_backup = mock_safe(CreateFileStorageBackup)
    mock_create_file_storage_backup.create_backup.side_effect = lambda x: Path(
        x
    ).touch()
    mock_create_db_backup = mock_safe(CreateDbBackup)
    mock_create_db_backup.create_backup.side_effect = lambda x: Path(x).touch()
    backup_creator = BackupCreator(
        mock_create_file_storage_backup, mock_create_db_backup
    )

    with pytest.raises(ValueError):
        backup_creator.create_backup(str(uuid.uuid4()))


def test_should_fail_if_provided_path_is_a_file(tmp_path):
    mock_create_file_storage_backup = mock_safe(CreateFileStorageBackup)
    mock_create_file_storage_backup.create_backup.side_effect = lambda x: Path(
        x
    ).touch()
    mock_create_db_backup = mock_safe(CreateDbBackup)
    mock_create_db_backup.create_backup.side_effect = lambda x: Path(x).touch()
    backup_creator = BackupCreator(
        mock_create_file_storage_backup, mock_create_db_backup
    )

    with pytest.raises(ValueError):
        backup_creator.create_backup(str((tmp_path / "a_file.txt").touch()))
