import os
import re
import subprocess
from typing import Dict, Tuple

from cato_common.utils.change_cwd import change_cwd


def _trim_output(output, trimmers: Dict[str, str]):
    if trimmers:
        output = output.split(r"\n")
        for pattern, replacement in trimmers.items():
            output = list(map(lambda x: re.sub(pattern, replacement, x), output))

    return output


def snapshot_output(
    snapshot, command, workdir=None, trimmers: Dict[str, str] = None, env=None
):
    with change_cwd(workdir if workdir else os.getcwd()):
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8",
            env=env,
        )

        if trimmers:
            output = _trim_output(output, trimmers)

        snapshot.assert_match(output)


def run_command(
    command, workdir=None, trimmers: Dict[str, str] = None, env=None
) -> Tuple[str, str, int]:
    with change_cwd(workdir if workdir else os.getcwd()):
        completed_process = subprocess.run(
            command, capture_output=True, universal_newlines=True, env=env
        )

        stdout = _trim_output(completed_process.stdout, trimmers)
        stderr = _trim_output(completed_process.stderr, trimmers)

        return stdout, stderr, completed_process.returncode
