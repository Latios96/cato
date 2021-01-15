import os
from unittest import mock

from cato.runners.command_runner import CommandRunner, CommandResult, LogLinesCollector


def create_cmd(script_name):
    return "python {}".format(os.path.join(os.path.dirname(__file__), script_name))


def test_command_runner_success():
    cmd = create_cmd("demo_script.py")
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(mock_output_processor)

    result = command_runner.run(cmd)

    assert result == CommandResult(
        cmd, 0, ["0\n", "1\n", "2\n", "3\n", "4\n", "5\n", "6\n", "7\n", "8\n", "9\n"]
    )


def test_read_from_stdout_only():
    cmd = create_cmd("stdout_only.py")
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(mock_output_processor)

    result = command_runner.run(cmd)

    assert result == CommandResult(cmd, 0, ["Hello world from STDOUT"])


def test_read_from_stderr_only():
    cmd = create_cmd("stderr_only.py")
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(mock_output_processor)

    result = command_runner.run(cmd)

    assert result == CommandResult(cmd, 0, ["Hello world from STDERR"])


def test_read_from_both():
    cmd = create_cmd("stdout_and_stderr.py")
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(mock_output_processor)

    result = command_runner.run(cmd)

    assert set(result.output) == {
        "Hello world from STDOUT\n",
        "Hello world from STDERR\n",
    }


def test_log_line_collector():
    log_lines_collector = LogLinesCollector(10)
    for i in range(11):
        log_lines_collector.append(str(i))

    assert log_lines_collector.lines == [
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        "Log does contain more than maximum of 10 lines, capping log..",
    ]
