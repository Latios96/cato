import os

from cato.commands.base_command import BaseCliCommand
from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from tests.utils import mock_safe


def test_read_config_should_populate_run_config_correctly(test_resource_provider):
    config_directory = test_resource_provider.resource_by_name("cato_test_config")
    base_command = BaseCliCommand(JsonConfigParser())

    run_config = base_command._read_config(config_directory, None)

    assert run_config == RunConfig(
        project_name="Example",
        resource_path=config_directory,
        suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="python --version",
                        variables={},
                        comparison_settings=ComparisonSettings(
                            method=ComparisonMethod.SSIM, threshold=0.8
                        ),
                    )
                ],
                variables={},
            )
        ],
        output_folder=os.getcwd(),
        variables={},
    )


def test_should_add_cli_vars_to_project(test_resource_provider, config_fixture):
    config_directory = test_resource_provider.resource_by_name("cato_test_config")
    cli_variables = {"my_custom_var": "my_custom_value"}
    base_command = BaseCliCommand(JsonConfigParser())

    run_config = base_command._read_config(
        config_directory,
        cli_variables=cli_variables,
    )

    assert run_config == RunConfig(
        project_name="Example",
        resource_path=config_directory,
        suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="python --version",
                        variables={},
                        comparison_settings=ComparisonSettings(
                            method=ComparisonMethod.SSIM, threshold=0.8
                        ),
                    )
                ],
                variables={},
            )
        ],
        output_folder=os.getcwd(),
        variables={"my_custom_var": "my_custom_value"},
    )


def test_should_override_project_vars_with_cli_vars(
    test_resource_provider, config_fixture
):
    config_directory = test_resource_provider.resource_by_name("cato_test_config")
    mocked_parser = mock_safe(JsonConfigParser)
    config = config_fixture.CONFIG
    config.variables["my_custom_var"] = "value_before"
    mocked_parser.parse.return_value = config
    cli_variables = {"my_custom_var": "my_custom_value"}
    base_command = BaseCliCommand(mocked_parser)

    run_config = base_command._read_config(
        config_directory,
        cli_variables=cli_variables,
    )

    assert run_config == RunConfig(
        project_name="EXAMPLE_PROJECT",
        resource_path=config_directory,
        suites=[config_fixture.TEST_SUITE],
        output_folder=os.getcwd(),
        variables={
            "my_var": "from_config",
            "my_custom_var": "my_custom_value",
        },
    )
