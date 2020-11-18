import os

from cato.domain.config import Config
from cato.domain.test import Test
from cato.domain.test_suite import TestSuite
from cato.runners.variable_processor import VariableProcessor


def test_evaluate_variables_no_custom_vars():
    config = Config(path="config_path", test_suites=[], output_folder="test")
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test("test_name", "test_command", variables={})
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.path,
        "output_folder": "test",
        "test_resources": "config_path/my_test_suite/test_name",
        "image_output_folder": "test/result/my_test_suite/test_name",
        "image_output_no_extension": "test/result/my_test_suite/test_name/test_name",
        "image_output_png": "test/result/my_test_suite/test_name/test_name.png",
        "image_output_exr": "test/result/my_test_suite/test_name/test_name.exr",
        "reference_image_exr": "config_path/my_test_suite/test_name/reference.exr",
        "reference_image_no_extension": "config_path/my_test_suite/test_name/reference",
        "reference_image_png": "config_path/my_test_suite/test_name/reference.png",
    }


def test_evaluate_variables_custom_image_output():
    config = Config(path="config_path", test_suites=[], output_folder="test")
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test(
        "test_name",
        "test_command",
        variables={
            "frame": "7",
            "image_output_png": "{@image_output_folder}/test_name{@frame}.png",
        },
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(
        config,
        suite,
        test,
    )

    assert variables == {
        "frame": "7",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.path,
        "output_folder": "test",
        "test_resources": "config_path/my_test_suite/test_name",
        "image_output_folder": "test/result/my_test_suite/test_name",
        "image_output_no_extension": "test/result/my_test_suite/test_name/test_name",
        "image_output_png": "test/result/my_test_suite/test_name/test_name7.png",
        "image_output_exr": "test/result/my_test_suite/test_name/test_name.exr",
        "reference_image_exr": "config_path/my_test_suite/test_name/reference.exr",
        "reference_image_no_extension": "config_path/my_test_suite/test_name/reference",
        "reference_image_png": "config_path/my_test_suite/test_name/reference.png",
    }


def test_format_command():
    variable_processor = VariableProcessor()

    command = variable_processor.format_command(
        "{@image_output_png}", {"image_output_png": "test"}
    )

    assert command == "test"
