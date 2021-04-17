import json
import os
from io import StringIO

import pytest
from jsonschema import ValidationError

from cato.config.config_file_parser import JsonConfigParser
from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


TEST_JSON = "test/test.json"

EXAMPLE_PROJECT = "example project"

VALID_CONFIG = {
    "project_name": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                }
            ],
        }
    ],
}

EXPECTED_VALID_CONFIG = Config(
    project_name=EXAMPLE_PROJECT,
    test_suites=[
        TestSuite(
            name="My_first_test_Suite",
            tests=[
                Test(
                    name="My_first_test",
                    command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    variables={},
                )
            ],
        )
    ],
)

VALID_CONFIG_WITH_VARIABLES = {
    "project_name": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    "variables": {"frame": "7"},
                }
            ],
        }
    ],
}

VALID_CONFIG_WITH_VARIABLES_IN_SUITE_AND_TEST = {
    "project_name": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    "variables": {"frame": "7"},
                }
            ],
            "variables": {"my_var": "from_suite"},
        }
    ],
    "variables": {"my_var": "from_config"},
}

INVALID_CONFIG = {
    "suite": {
        "name": "My_first_test_Suite",
        "tests": [
            {
                "name": "My_first_test",
                "cmd": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
            }
        ],
    }
}


def test_success():
    json_config_parser = JsonConfigParser()

    suites = json_config_parser.parse(TEST_JSON, StringIO(json.dumps(VALID_CONFIG)))

    assert suites == EXPECTED_VALID_CONFIG


def test_success_with_variables():
    json_config_parser = JsonConfigParser()

    suites = json_config_parser.parse(
        TEST_JSON, StringIO(json.dumps(VALID_CONFIG_WITH_VARIABLES))
    )

    assert suites == Config(
        project_name=EXAMPLE_PROJECT,
        test_suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                        variables={"frame": "7"},
                    )
                ],
            )
        ],
    )


def test_success_with_variables_in_config_and_suite():
    json_config_parser = JsonConfigParser()

    suites = json_config_parser.parse(
        TEST_JSON,
        StringIO(json.dumps(VALID_CONFIG_WITH_VARIABLES_IN_SUITE_AND_TEST)),
    )

    assert suites == Config(
        project_name=EXAMPLE_PROJECT,
        test_suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                        variables={"frame": "7"},
                    )
                ],
                variables={"my_var": "from_suite"},
            )
        ],
        variables={"my_var": "from_config"},
    )


def test_failure():
    json_config_parser = JsonConfigParser()

    with pytest.raises(ValidationError):
        json_config_parser.parse("test", StringIO(json.dumps(INVALID_CONFIG)))


def test_success_parse_dict():
    json_config_parser = JsonConfigParser()

    suites = json_config_parser.parse_dict(VALID_CONFIG)

    assert suites == EXPECTED_VALID_CONFIG


def test_failure_parse_dict():
    json_config_parser = JsonConfigParser()

    with pytest.raises(ValidationError):
        json_config_parser.parse_dict(INVALID_CONFIG)
