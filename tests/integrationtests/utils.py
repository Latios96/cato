import os
import re
import subprocess
from typing import Dict, Tuple, MutableMapping, Optional

from tenacity import RetryCallState, _utils

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
    env = _strip_github_actions_from_env(env)
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
    env = _strip_github_actions_from_env(env)
    with change_cwd(workdir if workdir else os.getcwd()):
        completed_process = subprocess.run(
            command, capture_output=True, universal_newlines=True, env=env
        )

        stdout = _trim_output(completed_process.stdout, trimmers)
        stderr = _trim_output(completed_process.stderr, trimmers)

        return stdout, stderr, completed_process.returncode


def tenacity_before_print():
    def print_it(retry_state: "RetryCallState") -> None:
        print(f"Starting call to '{_utils.get_callback_name(retry_state.fn)}'")
        print(
            f"this is the {_utils.to_ordinal(retry_state.attempt_number)} time calling it."
        )

    return print_it


def _strip_github_actions_from_env(
    env: Optional[MutableMapping[str, str]]
) -> MutableMapping[str, str]:
    if not env:
        env = os.environ.copy()
    if "GITHUB_ACTIONS" in env.keys():
        env.pop("GITHUB_ACTIONS")
    return env
