from unittest import mock

import pytest

from cato_server.backup.pg_dump_path_resolver import PgDumpPathResolver


def test_should_resolve_to_given_hint():
    pg_dump_path_resolver = PgDumpPathResolver()

    resolved_path = pg_dump_path_resolver.resolve(__file__)

    assert resolved_path == __file__


@mock.patch("shutil.which")
def test_should_resolve_to_pg_dump_from_oath(mock_shutil_which):
    mock_shutil_which.return_value = "pg_dump"
    pg_dump_path_resolver = PgDumpPathResolver()

    resolved_path = pg_dump_path_resolver.resolve(None)

    assert resolved_path == "pg_dump"
    mock_shutil_which.assert_called_with("pg_dump")


@mock.patch("shutil.which")
@mock.patch("glob.glob")
@mock.patch("platform.system")
def test_should_resolve_to_windows_default_installation_location(
    mock_platform_system, mock_glob_glob, mock_shutil_which
):
    mock_shutil_which.return_value = None
    mock_glob_glob.return_value = [r"C:\Program Files\PostgreSQL\13\bin\pg_dump.exe"]
    mock_platform_system.return_value = "Windows"
    pg_dump_path_resolver = PgDumpPathResolver()

    resolved_path = pg_dump_path_resolver.resolve(None)

    assert resolved_path == r"C:\Program Files\PostgreSQL\13\bin\pg_dump.exe"
    mock_glob_glob.assert_called_with(r"C:\Program Files\PostgreSQL\*\bin\pg_dump.exe")
    mock_shutil_which.assert_called_with("pg_dump")


@mock.patch("shutil.which")
@mock.patch("glob.glob")
@mock.patch("platform.system")
def test_should_throw_exception_because_no_executable_could_be_found(
    mock_platform_system, mock_glob_glob, mock_shutil_which
):
    mock_shutil_which.return_value = None
    mock_glob_glob.return_value = []
    mock_platform_system.return_value = "Windows"
    pg_dump_path_resolver = PgDumpPathResolver()

    with pytest.raises(RuntimeError):
        pg_dump_path_resolver.resolve(None)

    mock_glob_glob.assert_called_with(r"C:\Program Files\PostgreSQL\*\bin\pg_dump.exe")
    mock_shutil_which.assert_called_with("pg_dump")
