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

        stdout = popen.stdout
        stderr = popen.stderr
        assert stdout and stderr
        while popen.poll() is None:
            lines_iterator = iter(stdout.readline, "")
            for line in lines_iterator:
                self._lines.append(line)
                self._output_processor.process(line)

            lines_iterator = iter(stderr.readline, "")
            for line in lines_iterator:
                self._lines.append(line)
                self._output_processor.process(line)
        stdout.close()
        stderr.close()
        return_code = popen.wait()
        return CommandResult(cmd, return_code, self._lines)
