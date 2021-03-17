import contextlib
import os
import re
import subprocess
from typing import Dict, Tuple


@contextlib.contextmanager
def change_cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_cwd)


def _trim_output(output, trimmers: Dict[str, str]):
    if trimmers:
        output = output.split(r"\n")
        for pattern, replacement in trimmers.items():
            output = list(map(lambda x: re.sub(pattern, replacement, x), output))

    return output


def snapshot_output(snapshot, command, workdir=None, trimmers: Dict[str, str] = None):
    with change_cwd(workdir if workdir else os.getcwd()):
        output = subprocess.check_output(
            command, stderr=subprocess.STDOUT, universal_newlines=True, encoding="utf-8"
        )

        if trimmers:
            output = _trim_output(output, trimmers)

        snapshot.assert_match(output)


def run_command(
    command, workdir=None, trimmers: Dict[str, str] = None
) -> Tuple[str, str, int]:
    with change_cwd(workdir if workdir else os.getcwd()):
        completed_process = subprocess.run(
            command, capture_output=True, universal_newlines=True
        )

        stdout = _trim_output(completed_process.stdout, trimmers)
        stderr = _trim_output(completed_process.stderr, trimmers)

        return stdout, stderr, completed_process.returncode
