from subprocess import CompletedProcess
from unittest import mock

import pytest

from cato_server.backup.create_file_storage_backup import CreateFileStorageBackup
from cato_server.configuration.storage_configuration import StorageConfiguration


@pytest.fixture
def create_filestorage_backup_setup():
    storage_configuration = StorageConfiguration(
        file_storage_url="file_storage_url",
        database_url="postgresql+psycopg2://postgres:postgres@localhost:5432/cato-example",
    )
    create_filestorage_backup = CreateFileStorageBackup(storage_configuration)
    with mock.patch("subprocess.run") as mock_subprocess_run:
        yield create_filestorage_backup, mock_subprocess_run


def test_should_create_archive_correctly(create_filestorage_backup_setup, tmp_path):
    create_filestorage_backup, mock_subprocess_run = create_filestorage_backup_setup
    db_backup_path = str(tmp_path / "backup.tar")
    mock_subprocess_run.return_value = CompletedProcess([], 0)

    create_filestorage_backup.create_backup(db_backup_path)

    mock_subprocess_run.assert_called_once()
    assert mock_subprocess_run.call_args[0] == (
        f"tar -cf {db_backup_path} -C file_storage_url .",
    )


def test_should_raise_exception_if_archive_creation_failed(
    create_filestorage_backup_setup, tmp_path
):
    create_filestorage_backup, mock_subprocess_run = create_filestorage_backup_setup
    db_backup_path = str(tmp_path / "backup.tar")
    mock_subprocess_run.return_value = CompletedProcess([], 1)

    with pytest.raises(Exception):
        create_filestorage_backup.create_backup(db_backup_path)

    mock_subprocess_run.assert_called_once()
    assert mock_subprocess_run.call_args[0] == (
        f"tar -cf {db_backup_path} -C file_storage_url .",
    )


@mock.patch("shutil.which")
def test_should_raise_exception_if_tar_command_is_not_found(
    mock_shutil_which, create_filestorage_backup_setup, tmp_path
):
    mock_shutil_which.return_value = None
    create_filestorage_backup, mock_subprocess_run = create_filestorage_backup_setup
    db_backup_path = str(tmp_path / "backup.tar")
    mock_subprocess_run.return_value = CompletedProcess([], 1)

    with pytest.raises(RuntimeError):
        create_filestorage_backup.create_backup(db_backup_path)

    mock_subprocess_run.assert_not_called()
