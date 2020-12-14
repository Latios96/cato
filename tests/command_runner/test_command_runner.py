import os
from unittest import mock

from cato.runners.command_runner import CommandRunner, CommandResult


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

    assert result == CommandResult(
        cmd, 0, ["Hello world from STDOUT", "Hello world from STDERR"]
    )
