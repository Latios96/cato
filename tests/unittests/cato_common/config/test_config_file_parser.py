import json
from io import StringIO

import pytest
from jsonschema import ValidationError

from cato_common.config.config_file_parser import JsonConfigParser
from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import Config
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite

TEST_JSON = "test/test.json"

EXAMPLE_PROJECT = "example project"

VALID_CONFIG = {
    "projectName": EXAMPLE_PROJECT,
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
    suites=[
        TestSuite(
            name="My_first_test_Suite",
            tests=[
                Test(
                    name="My_first_test",
                    command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    variables={},
                    comparison_settings=ComparisonSettings.default(),
                )
            ],
        )
    ],
)

VALID_CONFIG_WITH_VARIABLES = {
    "projectName": EXAMPLE_PROJECT,
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
    "projectName": EXAMPLE_PROJECT,
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

VALID_CONFIG_NO_COMPARISON_SETTINGS = {
    "projectName": EXAMPLE_PROJECT,
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

VALID_CONFIG_WITH_COMPARISON_SETTINGS = {
    "projectName": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    "comparisonSettings": {"method": "SSIM", "threshold": 0.2},
                }
            ],
        }
    ],
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

INVALID_COMPARISON_METHOD = {
    "projectName": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    "comparison_settings": {"method": "INVALID", "threshold": 0.1},
                }
            ],
        }
    ],
}

INVALID_COMPARISON_THRESHOLD = {
    "projectName": EXAMPLE_PROJECT,
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {
                    "name": "My_first_test",
                    "command": "mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                    "comparison_settings": {"method": "SSIM", "threshold": "0.1"},
                }
            ],
        }
    ],
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
        suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                        variables={"frame": "7"},
                        comparison_settings=ComparisonSettings.default(),
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
        suites=[
            TestSuite(
                name="My_first_test_Suite",
                tests=[
                    Test(
                        name="My_first_test",
                        command="mayabatch -s {config_file_folder}/{test_name.json} -o {image_output}/{test_name.png}",
                        variables={"frame": "7"},
                        comparison_settings=ComparisonSettings.default(),
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


def test_parse_invalid_comparison_method():
    json_config_parser = JsonConfigParser()

    with pytest.raises(ValidationError):
        json_config_parser.parse_dict(INVALID_COMPARISON_METHOD)


def test_parse_invalid_comparison_threshold():
    json_config_parser = JsonConfigParser()

    with pytest.raises(ValidationError):
        json_config_parser.parse_dict(INVALID_COMPARISON_THRESHOLD)


def test_parse_no_comparison_settings():
    json_config_parser = JsonConfigParser()

    config = json_config_parser.parse_dict(VALID_CONFIG_NO_COMPARISON_SETTINGS)

    test = config.suites[0].tests[0]
    assert test.comparison_settings == ComparisonSettings.default()


def test_parse_use_defined_comparison_settings():
    json_config_parser = JsonConfigParser()

    config = json_config_parser.parse_dict(VALID_CONFIG_WITH_COMPARISON_SETTINGS)

    test = config.suites[0].tests[0]
    assert test.comparison_settings == ComparisonSettings(
        method=ComparisonMethod.SSIM, threshold=0.2
    )
