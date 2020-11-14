import subprocess
from dataclasses import dataclass
from typing import List

from cato.runners.output_processor import OutputProcessor


@dataclass
class CommandResult:
    cmd: str
    exit_code: int
    output: List[str]


class CommandRunner:
    def __init__(self, output_processor: OutputProcessor):
        self._output_processor = output_processor

    def run(self, cmd: str) -> CommandResult:
        self._lines = []
        popen = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            shell=True,
        )

        while popen.poll() is None:
            line = popen.stdout.readline()
            if line != "":
                self._lines.append(line)
                self._output_processor.process(line)
            line = popen.stderr.readline()
            if line != "":
                self._lines.append(line)
                self._output_processor.process(line)
        popen.stdout.close()
        return_code = popen.wait()
        return CommandResult(cmd, return_code, self._lines)
