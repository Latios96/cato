import sys

import pytest

from tests.integrationtests.command_fixture import run_command, CommandResult


def test_run_command_should_collect_output():
    result = run_command([sys.executable, "--version"])

    assert result.exit_code == 0
    assert result.output[0].startswith("Python")


class TestCommandResult:
    @pytest.mark.parametrize(
        "lines,line_to_contain",
        [
            (["1\n", "2\n", "3\n", "4\n", "5\n"], "1"),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], "1\n"),
            (["1\n", "1\n", "1\n", "1\n", "1\n"], "1"),
            (["1\n", "1\n", "1\n", "1\n", "1\n"], "1\n"),
        ],
    )
    def test_output_should_contain_line(self, lines, line_to_contain):
        result = CommandResult(0, lines)

        assert result.output_contains_line(line_to_contain)

    def test_output_should_not_contain_line(self):
        result = CommandResult(0, ["1\n", "2\n", "3\n" "4\n" "5\n"])

        assert not result.output_contains_line("6")
        assert not result.output_contains_line("6\n")

    @pytest.mark.parametrize(
        "lines,pattern_to_contain",
        [
            (["1\n", "2\n", "3\n", "4\n", "5\n"], "1"),
            (["1\n", "1\n", "1\n", "1\n", "1\n"], "1"),
            (["1\n", "1\n", "1\n", "1\n", "1\n"], "1\n"),
            (["123\n", "456\n", "789\n", "10\n", "11\n"], "1.*"),
            (["123\n", "456\n", "789\n", "10\n", "11\n"], "1\d"),
            (["abc\n", "456\n", "d\n", "10\n", "11\n"], "1\d$"),
        ],
    )
    def test_output_should_contain_line_matching(self, lines, pattern_to_contain):
        result = CommandResult(0, lines)

        assert result.output_contains_line_matching(pattern_to_contain)

    @pytest.mark.parametrize(
        "lines,pattern_to_contain",
        [
            (["1\n", "2\n", "3\n", "4\n", "5\n"], "a"),
            (["23\n", "456\n", "789\n", "0\n", "2\n"], "1.*"),
        ],
    )
    def test_output_should_not_contain_line_matching(self, lines, pattern_to_contain):
        result = CommandResult(0, lines)

        assert not result.output_contains_line_matching(pattern_to_contain)

    @pytest.mark.parametrize(
        "lines,lines_to_contain",
        [
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["1"]),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["1", "2"]),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["1\n", "2\n"]),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["3", "4"]),
            (["3\n", "4\n", "3\n", "4\n", "5\n"], ["3", "4"]),
            (["3\n", "4\n", "5\n", "6\n", "7\n", "8" "3", "4"], ["3", "4"]),
        ],
    )
    def test_output_contains_lines(self, lines, lines_to_contain):
        result = CommandResult(0, lines)

        assert result.output_contains_lines(lines_to_contain)

    @pytest.mark.parametrize(
        "lines,lines_to_contain",
        [
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["8"]),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["2", "1"]),
            (["1\n", "2\n", "3\n", "4\n", "5\n"], ["4", "2"]),
            (["3\n", "4\n", "5\n", "6\n", "7\n", "8" "3", "4"], ["4", "3"]),
        ],
    )
    def test_output_should_not_contains_lines(self, lines, lines_to_contain):
        result = CommandResult(0, lines)

        assert not result.output_contains_lines(lines_to_contain)
