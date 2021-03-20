import re
import subprocess
import sys
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import List


@dataclass
class CommandResult:
    exit_code: int
    output: List[str]

    def output_contains_line(self, str_to_contain: str) -> bool:
        for line in self.output:
            if str_to_contain in line:
                return True
        return False

    def output_contains_line_matching(self, pattern_to_contain: str) -> bool:
        for line in self.output:
            if re.search(pattern_to_contain, line) is not None:
                return True
        return False

    def output_contains_lines(self, lines_to_contain: List[str]) -> bool:
        clean_output = list(map(lambda x: x.rstrip("\n"), self.output))
        clean_lines_to_contain = list(map(lambda x: x.rstrip("\n"), lines_to_contain))
        matcher = SequenceMatcher(a=clean_output, b=clean_lines_to_contain)

        longest_match = matcher.find_longest_match(
            0, len(self.output), 0, len(lines_to_contain)
        )
        return longest_match.size == len(lines_to_contain)


def run_command(cmd: List[str]) -> CommandResult:
    output_lines = []
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
            output_lines.append(line)
    stdout.close()
    return_code = popen.wait()
    return CommandResult(exit_code=return_code, output=output_lines)


def run_cato_command(cmd: List[str]) -> CommandResult:
    cato_cmd = [
        sys.executable,
        "-m",
        "cato",
    ]
    cato_cmd.extend(cmd)
    return run_command(cato_cmd)
