import os

from cato.commands.base_command import BaseCliCommand
from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite


def test_read_config_should_populate_run_config_correctly(test_resource_provider):
    config_directoy = test_resource_provider.resource_by_name("cato_test_config")

    base_command = BaseCliCommand(JsonConfigParser())
    run_config = base_command._read_config(config_directoy)

    assert run_config == RunConfig(
        project_name="Example",
        resource_path=config_directoy,
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
