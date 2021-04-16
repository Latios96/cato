import os
import sys

import pytest

from cato.config.config_encoder import ConfigEncoder
from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from cato.reporter.test_execution_db_reporter import TestExecutionDbReporter
from cato.utils.machine_info_collector import MachineInfoCollector
from cato_api_client.cato_api_client import CatoApiClient
from cato_api_client.http_template import HttpTemplate
from cato_server.mappers.mapper_registry_factory import MapperRegistryFactory
from cato_server.mappers.object_mapper import ObjectMapper
from tests.integrationtests.utils import snapshot_output, run_command


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


@pytest.mark.skipif(
    sys.platform != "win32", reason="not working on linux, to be removed anyway"
)
def test_submit_command(live_server, snapshot, run_config, test_resource_provider):
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
    )


def test_worker_run_command(live_server, snapshot, run_config):
    object_mapper = ObjectMapper(MapperRegistryFactory().create_mapper_registry())
    execution_reporter = TestExecutionDbReporter(
        MachineInfoCollector(),
        CatoApiClient(
            live_server.server_url(), HttpTemplate(object_mapper), object_mapper
        ),
    )
    parser = JsonConfigParser()
    config = parser.parse(run_config)
    execution_reporter.start_execution("test", config.test_suites)
    config_encoder = ConfigEncoder(ConfigFileWriter(), parser)

    command = [
        sys.executable,
        "-m",
        "cato",
        "worker-run",
        "-u",
        live_server.server_url(),
        "-config",
        config_encoder.encode(config).decode(),
        "-test-identifier",
        "PythonTestSuite/PythonOutputVersion",
        "-run-id",
        "{}".format(execution_reporter._run_id),
        "-resource-path",
        os.getcwd(),
    ]

    stdout, stderr, exit_code = run_command(
        command,
        os.path.dirname(os.path.dirname(run_config)),
        trimmers={
            "succeeded in.*": "succeeded in 0.12 seconds",
            "passed in.*": "passed in 0.12 seconds",
            "Command: .*": "Command: <some command>",
            "Copy .* to .*": "Copy <a> to <b>",
        },
    )

    assert exit_code == 0
    snapshot.assert_match(stderr)
