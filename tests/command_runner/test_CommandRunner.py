import os
from unittest import mock

from cato.runners.CommandRunner import CommandRunner, CommandResult


def test_command_runner_success():
    cmd = ["python", os.path.join(os.path.dirname(__file__), "demo_script.py")]
    mock_output_processor = mock.MagicMock()
    command_runner = CommandRunner(cmd, mock_output_processor)

    result = command_runner.run()

    assert result == CommandResult(
        cmd, 0, ["0\n", "1\n", "2\n", "3\n", "4\n", "5\n", "6\n", "7\n", "8\n", "9\n"]
    )
