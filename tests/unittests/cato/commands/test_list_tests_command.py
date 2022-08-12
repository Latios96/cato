import copy
import logging
from unittest.mock import call

from cato.commands.list_tests_command import ListTestsCommand
from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.domain.comparison_settings import ComparisonSettings
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from tests.utils import mock_safe

TEST = Test(
    name="My_first_test",
    command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
    variables={"frame": "7"},
    comparison_settings=ComparisonSettings.default(),
)
TEST_SUITE = TestSuite(
    name="My_first_test_Suite",
    tests=[TEST],
    variables={"my_var": "from_suite"},
)
CONFIG = Config(
    project_name="EXAMPLE_PROJECT",
    suites=[TEST_SUITE],
    variables={"my_var": "from_config"},
)


def test_list_tests():
    config = copy.deepcopy(CONFIG)
    mock_json_config_parser = mock_safe(JsonConfigParser)
    mock_logger = mock_safe(logging.Logger)
    list_tests_command = ListTestsCommand(
        mock_json_config_parser,
        mock_logger,
    )
    mock_json_config_parser.parse.return_value = config

    list_tests_command.list_tests("my_path")

    mock_logger.info.assert_has_calls(
        [
            call("Found 1 tests in 1 suites:"),
            call(""),
            call("My_first_test_Suite/My_first_test"),
        ]
    )
