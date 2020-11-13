import subprocess
from dataclasses import dataclass
from typing import List, Callable


@dataclass
class CommandResult:
    cmd: List[str]
    exit_code: int
    output: List[str]


class CommandRunner:
    def __init__(self, cmd: List[str], output_processor: Callable[[str], None]):
        self._cmd = cmd
        self._output_processor = output_processor
        self._lines = []

    def run(self) -> CommandResult:
        popen = subprocess.Popen(
            self._cmd, stdout=subprocess.PIPE, universal_newlines=True
        )
        for stdout_line in iter(popen.stdout.readline, ""):
            self._lines.append(stdout_line)
            self._output_processor(stdout_line)
        popen.stdout.close()
        return_code = popen.wait()
        return CommandResult(self._cmd, return_code, self._lines)
