import contextlib
import os
import subprocess
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
            command, stderr=subprocess.STDOUT, universal_newlines=True, encoding="utf-8"
        )

        if trimmers:
            for key, value in trimmers.items():
                output = output.replace(key, value)

        snapshot.assert_match(output)
