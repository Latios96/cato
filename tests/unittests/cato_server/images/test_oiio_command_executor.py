from unittest import mock

import pytest

from cato_server.images.oiio_command_executor import (
    OiioCommandExecutor,
    NotAnImageException,
)


@mock.patch("subprocess.getstatusoutput")
def test_exit_code_zero_no_error_output_should_pass(mock_getstatusoutput):
    mock_getstatusoutput.return_value = (1, "oiiotool output")
    oiio_command_executor = OiioCommandExecutor()

    output = oiio_command_executor.execute_command("command")

    assert output == "oiiotool output"


@mock.patch("subprocess.getstatusoutput")
def test_non_zero_exit_code(mock_getstatusoutput):
    mock_getstatusoutput.return_value = (1, "oiiotool ERROR")
    oiio_command_executor = OiioCommandExecutor()

    with pytest.raises(Exception):
        oiio_command_executor.execute_command("command")


@mock.patch("subprocess.getstatusoutput")
def test_not_an_image_error(mock_getstatusoutput):
    mock_getstatusoutput.return_value = (1, "oiiotool ERROR Not a PNG file")
    oiio_command_executor = OiioCommandExecutor()

    with pytest.raises(NotAnImageException):
        oiio_command_executor.execute_command("command")
