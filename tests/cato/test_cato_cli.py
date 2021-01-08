import contextlib
import os
import subprocess
import sys

from typing import Dict


@contextlib.contextmanager
def change_cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_cwd)


def snapshot_output(snapshot, command, workdir=None, trimmers: Dict[str, str] = None):
    with change_cwd(workdir if workdir else os.getcwd()):
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

        if trimmers:
            for key, value in trimmers.items():
                output = output.replace(key, value)

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


def test_config_file_template(snapshot, tmp_path):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "config-template", "."],
        workdir=str(tmp_path),
        trimmers={
            os.path.join(str(tmp_path), "cato.json"): "SOME_RANDOM_DIR/cato.json"
        },
    )
