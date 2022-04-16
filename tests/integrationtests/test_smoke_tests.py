import os
import sys

import cato_server
from tests.integrationtests.command_fixture import run_command


def test_smoke_test_cato_beat():
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(cato_server.__file__), "cato_beat.py"),
        "-h",
    ]
    return run_command(cmd)


def test_smoke_test_cato_server_admin():
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(cato_server.__file__), "cato_server_admin.py"),
        "-h",
    ]
    return run_command(cmd)


def test_smoke_test_cato_server():
    cmd = [
        sys.executable,
        os.path.join(os.path.dirname(cato_server.__file__), "__main__.py"),
        "-h",
    ]
    return run_command(cmd)
