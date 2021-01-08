import contextlib
import os
import subprocess
import sys


@contextlib.contextmanager
def change_cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_cwd)


def snapshot_output(snapshot, command, workdir=None):
    with change_cwd(workdir if workdir else os.getcwd()):
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
        snapshot.assert_match(output)


def test_list_tests_command_from_path(snapshot, config_file_fixture):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "list-tests", "--path", config_file_fixture],
    )


def test_list_tests_command_from_cwd(snapshot, config_file_fixture):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "list-tests"],
        workdir=os.path.dirname(config_file_fixture),
    )
