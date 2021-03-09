import os
import subprocess
import sys

import pytest
import requests

from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from tests.integrationtests.utils import change_cwd, snapshot_output


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
        name="PythonOutputVersion",  # copy image script
        command=f"python {os.path.join(os.path.dirname(__file__), 'copy_image.py')} {test_resource_provider.resource_by_name('test_image_black.png')} {{@image_output_png}}",
        variables={
            "reference_image_png": test_resource_provider.resource_by_name(
                "test_image_black.png"
            )
        },
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


def test_run_command(live_server, snapshot, run_config, test_resource_provider):
    with change_cwd(os.path.dirname(os.path.dirname(run_config))):
        output = subprocess.call(
            [
                sys.executable,
                "-m",
                "cato",
                "run",
                "--path",
                run_config,
                "-u",
                live_server.server_url(),
            ],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )

    assert requests.get(
        live_server.server_url() + "/api/v1/test_results/run/2"
    ).json() == [
        {
            "execution_status": "FINISHED",
            "id": 1,
            "name": "PythonOutputVersion",
            "status": "SUCCESS",
            "test_identifier": "PythonTestSuite/PythonOutputVersion",
        }
    ]


def test_worker_run_command(live_server, snapshot, run_config):
    with change_cwd(os.path.dirname(os.path.dirname(run_config))):
        output = subprocess.call(
            [
                sys.executable,
                "-m",
                "cato",
                "worker-run",
                "-config",
                "-test_identifier",
                "-run_id",
                "-resource_path",
            ],
            stderr=subprocess.STDOUT,
            universal_newlines=True,
        )
