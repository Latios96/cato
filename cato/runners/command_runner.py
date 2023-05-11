import subprocess
from dataclasses import dataclass
from typing import List

from cato.runners.output_processor import OutputProcessor


@dataclass
class CommandResult:
    cmd: str
    exit_code: int
    output: List[str]


class LogLinesCollector:
    MAX_LINES = 150000

    def __init__(self, max=MAX_LINES):
        self._lines = []
        self._max = max
        self._has_reached = False

    def append(self, line):
        if not self._has_reached:
            self._lines.append(line)
            if len(self._lines) == self._max:
                self._has_reached = True
                self._lines.append(
                    f"Log does contain more than maximum of {self._max} lines, capping log.."
                )

    @property
    def lines(self):
        return self._lines


class CommandRunner:
    def __init__(self, output_processor: OutputProcessor):
        self._output_processor = output_processor

    def run(self, cmd: str) -> CommandResult:
        log_lines_collector = LogLinesCollector()
        popen = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            shell=True,
        )

        stdout = popen.stdout
        assert stdout
        while popen.poll() is None:
            lines_iterator = iter(stdout.readline, "")
            for line in lines_iterator:
                log_lines_collector.append(line)
                self._output_processor.process(line)
        stdout.close()
        return_code = popen.wait()
        return CommandResult(cmd, return_code, [cmd + "\n", *log_lines_collector.lines])
