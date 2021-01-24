import contextlib
import os
import subprocess
import sys

from typing import Dict

import pytest

from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


@contextlib.contextmanager
def change_cwd(path):
    old_cwd = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_cwd)


def snapshot_output(snapshot, command, workdir=None, trimmers: Dict[str, str] = None):
    with change_cwd(workdir if workdir else os.getcwd()):
        output = subprocess.check_output(
            command,
            stderr=subprocess.STDOUT,
            universal_newlines=True,
            encoding="utf-8"
        )

        if trimmers:
            for key, value in trimmers.items():
                output = output.replace(key, value)

        snapshot.assert_match(output)


def test_list_tests_command_from_path(snapshot, config_file_fixture):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "list-tests", "--path", config_file_fixture],
        workdir=os.path.dirname(os.path.dirname(config_file_fixture)),
    )


def test_list_tests_command_from_cwd(snapshot, config_file_fixture):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "list-tests"],
        workdir=os.path.dirname(config_file_fixture),
    )


def test_config_file_template(snapshot, tmp_path):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "config-template", "."],
        workdir=str(tmp_path),
        trimmers={
            os.path.join(str(tmp_path), "cato.json"): "SOME_RANDOM_DIR/cato.json"
        },
    )


def test_update_missing_reference_images_should_have_no_effect(
        snapshot, test_resource_provider
):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "update-missing-reference-images"],
        workdir=test_resource_provider.resource_by_name("cato_test_config"),
    )


def test_update_reference_should_have_no_effect(snapshot, test_resource_provider):
    snapshot_output(
        snapshot,
        [
            sys.executable,
            "-m",
            "cato",
            "update-reference",
            "--test-identifier",
            "My_first_test_Suite/My_first_test",
        ],
        workdir=test_resource_provider.resource_by_name("cato_test_config"),
    )


@pytest.fixture
def run_config(tmp_path, test_resource_provider):
    test1 = Test(
        name="PythonOutputVersion", # copy image script
        command=f"python {os.path.join(os.path.dirname(__file__), 'copy_image.py')} {test_resource_provider.resource_by_name('test_image_black.png')} {{@image_output_png}}",
        variables={"reference_image_png": test_resource_provider.resource_by_name('test_image_black.png')},
    )
    python_test_suite = TestSuite(
        name="PythonTestSuite",
        tests=[test1],
        variables={},
    )
    config = Config(
        project_name="EXAMPLE_PROJECT",
        path="test",
        test_suites=[python_test_suite],
        output_folder="output",
        variables={"my_var": "from_config"},
    )
    path = os.path.join(str(tmp_path), "cato.json")
    ConfigFileWriter().write_to_file(path, config)
    return path


# normal run
# verbose
# suite
# test identifier
# only failed


def test_run_command(live_server, snapshot, run_config,test_resource_provider):
    snapshot_output(
        snapshot,
        [sys.executable, "-m", "cato", "run", "--path", run_config, "-u", live_server.server_url(), "-v"],
        workdir=os.path.dirname(os.path.dirname(run_config)),
        trimmers={
            live_server.server_url(): "<SERVER-URL>",
            os.path.join(os.path.dirname(__file__), 'copy_image.py'): "<TEST-SCRIPT-PATH>",
            test_resource_provider.resource_by_name('test_image_black.png'): "<REFERENCE-IMAGE>"
        }
    )
    # verify on server
