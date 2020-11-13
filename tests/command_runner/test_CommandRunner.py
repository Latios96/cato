import os
from unittest import mock

from cato.runners.command_runner import CommandRunner, CommandResult


def test_command_runner_success():
    cmd = "python {}".format(os.path.join(os.path.dirname(__file__), "demo_script.py"))
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(mock_output_processor)

    result = command_runner.run(cmd)

    assert result == CommandResult(
        cmd, 0, ["0\n", "1\n", "2\n", "3\n", "4\n", "5\n", "6\n", "7\n", "8\n", "9\n"]
    )
