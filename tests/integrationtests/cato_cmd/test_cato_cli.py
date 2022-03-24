import os
import sys

import pytest

from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.config import RunConfig
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from tests.integrationtests.utils import snapshot_output, run_command


@pytest.fixture
def run_config(tmp_path, test_resource_provider, object_mapper):
    test1 = Test(
        name="PythonOutputVersion",  # copy image script
        command=f"python {os.path.join(os.path.dirname(__file__), 'copy_image.py')} {test_resource_provider.resource_by_name('test_image_black.png')} {{@image_output_png}}",
        variables={
            "reference_image_png": test_resource_provider.resource_by_name(
                "test_image_black.png"
            )
        },
        comparison_settings=ComparisonSettings.default(),
    )
    python_test_suite = TestSuite(
        name="PythonTestSuite",
        tests=[test1],
        variables={},
    )
    config = RunConfig(
        project_name="EXAMPLE_PROJECT",
        resource_path="test",
        suites=[python_test_suite],
        output_folder="output",
        variables={"my_var": "from_config"},
    )
    path = os.path.join(str(tmp_path), "cato.json")
    ConfigFileWriter(object_mapper).write_to_file(path, config)
    return path


@pytest.mark.skipif(
    sys.platform != "win32", reason="not working on linux, to be removed anyway"
)
def test_submit_command(
    live_server, snapshot, run_config, test_resource_provider, env_with_api_token
):
    snapshot_output(
        snapshot,
        [
            sys.executable,
            "-m",
            "cato",
            "submit",
            "--path",
            run_config,
            "-u",
            live_server.server_url(),
        ],
        workdir=test_resource_provider.resource_by_name("cato_test_config"),
        trimmers={r"127.0.0.1:\d+": "127.0.0.1:12345"},
        env=env_with_api_token,
    )


def test_worker_run_command(
    live_server, snapshot, run_config, test_resource_provider, env_with_api_token
):
    snapshot_output(
        snapshot,
        [
            sys.executable,
            "-m",
            "cato",
            "submit",
            "--path",
            run_config,
            "-u",
            live_server.server_url(),
        ],
        workdir=test_resource_provider.resource_by_name("cato_test_config"),
        trimmers={r"127.0.0.1:\d+": "127.0.0.1:12345"},
        env=env_with_api_token,
    )

    command = [
        sys.executable,
        "-m",
        "cato",
        "worker-run",
        "-u",
        live_server.server_url(),
        "-submission-info-id",
        "1",
        "-test-identifier",
        "PythonTestSuite/PythonOutputVersion",
    ]

    stdout, stderr, exit_code = run_command(
        command,
        os.path.dirname(os.path.dirname(run_config)),
        trimmers={
            "succeeded in.*": "succeeded in 0.12 seconds",
            "passed in.*": "passed in 0.12 seconds",
            "Command: .*": "Command: <some command>",
            "Copy .* to .*": "Copy <a> to <b>",
            "Found image output at path .*": "Found image output at path <foo>",
            "Found reference image at path .*": "Found image output at path <bar>",
        },
        env=env_with_api_token,
    )

    snapshot.assert_match(stderr)
    assert exit_code == 0
