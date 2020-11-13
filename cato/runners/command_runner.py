import subprocess
from dataclasses import dataclass
from typing import List

from cato.runners.output_processor import OutputProcessor


@dataclass
class CommandResult:
    cmd: List[str]
    exit_code: int
    output: List[str]


class CommandRunner:
    def __init__(self, output_processor: OutputProcessor):
        self._output_processor = output_processor

    def run(self, cmd: str) -> CommandResult:
        self._lines = []
        popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, universal_newlines=True, shell=True)
        for stdout_line in iter(popen.stdout.readline, ""):
            self._lines.append(stdout_line)
            self._output_processor.process(stdout_line)
        popen.stdout.close()
        return_code = popen.wait()
        return CommandResult(cmd, return_code, self._lines)
