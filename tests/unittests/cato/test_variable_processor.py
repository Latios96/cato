import pytest

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from cato.variable_processing.variable_predefinition import PREDEFINITIONS
from cato.variable_processing.variable_processor import (
    VariableProcessor,
    VariableSubstitutionRecursionDepthExceeded,
)

REFERENCE_IMAGE_PNG = "config_path/my_test_suite/test_name/reference.png"
REFERENCE_IMAGE_NO_EXTENSION = "config_path/my_test_suite/test_name/reference"
REFERENCE_IMAGE_EXR = "config_path/my_test_suite/test_name/reference.exr"
REFERENCE_IMAGE_JPG = "config_path/my_test_suite/test_name/reference.jpg"
REFERENCE_IMAGE_TIF = "config_path/my_test_suite/test_name/reference.tif"
IMAGE_OUTPUT_EXR = "test/result/my_test_suite/test_name/test_name.exr"
IMAGE_OUTPUT_PNG = "test/result/my_test_suite/test_name/test_name.png"
IMAGE_OUTPUT_JPG = "test/result/my_test_suite/test_name/test_name.jpg"
IMAGE_OUTPUT_TIF = "test/result/my_test_suite/test_name/test_name.tif"
IMAGE_OUTPUT_NO_EXTENSION = "test/result/my_test_suite/test_name/test_name"
IMAGE_OUTPUT_FOLDER = "test/result/my_test_suite/test_name"
SUITE_RESOURCES = "config_path/my_test_suite"
TEST_RESOURCES = "config_path/my_test_suite/test_name"
EXAMPLE_PROJECT = "Example project"


def test_evaluate_variables_no_custom_vars():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
    )
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test(
        "test_name",
        "test_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_evaluate_variables_custom_image_output():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
    )
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test(
        "test_name",
        "test_command",
        variables={
            "frame": "7",
            "image_output_png": "{{image_output_folder}}/test_name{{frame}}.png",
        },
        comparison_settings=ComparisonSettings.default(),
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
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": "test/result/my_test_suite/test_name/test_name7.png",
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_format_command():
    variable_processor = VariableProcessor()

    command = variable_processor.format_command(
        "{{image_output_png}}", {"image_output_png": "test"}
    )

    assert command == "test"


def test_evaluate_variables_variables_from_config():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
        variables={"test_variable": "my_value"},
    )
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test(
        "test_name",
        "test_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "test_variable": "my_value",
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_evaluate_variables_variables_from_suite():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
    )
    suite = TestSuite(
        name="my_test_suite", tests=[], variables={"test_variable": "my_value"}
    )
    test = Test(
        "test_name",
        "test_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "test_variable": "my_value",
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_evaluate_variables_variables_from_config_override_by_suite():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
        variables={"test_variable": "my_value_from_config"},
    )
    suite = TestSuite(
        name="my_test_suite",
        tests=[],
        variables={"test_variable": "my_value_from_suite"},
    )
    test = Test(
        "test_name",
        "test_command",
        variables={},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "test_variable": "my_value_from_suite",
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_evaluate_variables_variables_from_config_override_by_suite_overriden_by_test():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
        variables={"test_variable": "my_value_from_config"},
    )
    suite = TestSuite(
        name="my_test_suite",
        tests=[],
        variables={"test_variable": "my_value_from_suite"},
    )
    test = Test(
        "test_name",
        "test_command",
        variables={"test_variable": "my_value_from_test"},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(config, suite, test)

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "test_variable": "my_value_from_test",
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_evaluate_variables_maya_predefinition():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
        variables={"test_variable": "my_value_from_config"},
    )
    suite = TestSuite(
        name="my_test_suite",
        tests=[],
        variables={"test_variable": "my_value_from_suite"},
    )
    test = Test(
        "test_name",
        "test_command",
        variables={"test_variable": "my_value_from_test"},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    variables = variable_processor.evaluate_variables(
        config, suite, test, predefinitions=PREDEFINITIONS
    )

    assert variables == {
        "frame": "0001",
        "test_name": test.name,
        "suite_name": suite.name,
        "config_path": config.resource_path,
        "output_folder": "test",
        "suite_resources": SUITE_RESOURCES,
        "test_resources": TEST_RESOURCES,
        "image_output_folder": IMAGE_OUTPUT_FOLDER,
        "image_output_no_extension": IMAGE_OUTPUT_NO_EXTENSION,
        "image_output_png": IMAGE_OUTPUT_PNG,
        "image_output_exr": IMAGE_OUTPUT_EXR,
        "reference_image_exr": REFERENCE_IMAGE_EXR,
        "reference_image_no_extension": REFERENCE_IMAGE_NO_EXTENSION,
        "reference_image_png": REFERENCE_IMAGE_PNG,
        "test_variable": "my_value_from_test",
        "arnold_location": r"C:\Program Files\Autodesk\Arnold\maya2020",
        "arnold_render_command": r'"C:\Program Files\Autodesk\Arnold\maya2020\bin\kick" -i config_path/my_test_suite/test_name/test_name.ass -o test/result/my_test_suite/test_name/test_name.png -of exr -dw -v 2',
        "arnold_scene_file": "config_path/my_test_suite/test_name/test_name.ass",
        "blender_location": r"C:\Program Files\Blender Foundation\Blender 2.90",
        "blender_render_command": r'"C:\Program Files\Blender Foundation\Blender 2.90\blender.exe" -b  config_path/my_test_suite/test_name/test_name.blend -o test/result/my_test_suite/test_name/test_name -F PNG -f 0001',
        "blender_scene_file": "config_path/my_test_suite/test_name/test_name.blend",
        "blender_version": "2.90",
        "maya_location": r"C:\Program Files\Autodesk\Maya2020",
        "maya_version": "2020",
        "vray_render_command": r'"C:\Program Files\Autodesk\Maya2020\vray\bin\vray.exe" -sceneFile=config_path/my_test_suite/test_name/scene.vrscene -imgFile=test/result/my_test_suite/test_name/test_name.exr -progressIncrement=1 -display=0',
        "vray_gpu_render_command": r'"C:\Program Files\Autodesk\Maya2020\vray\bin\vray.exe" -sceneFile=config_path/my_test_suite/test_name/scene.vrscene -imgFile=test/result/my_test_suite/test_name/test_name.exr -progressIncrement=1 -display=0 -rtengine=5',
        "vray_scene_file": "config_path/my_test_suite/test_name/scene.vrscene",
        "image_output_jpg": IMAGE_OUTPUT_JPG,
        "image_output_tif": IMAGE_OUTPUT_TIF,
        "reference_image_jpg": REFERENCE_IMAGE_JPG,
        "reference_image_tif": REFERENCE_IMAGE_TIF,
    }


def test_raise_max_recursion_exceeded_for_cyclic_variables():
    config = RunConfig(
        project_name=EXAMPLE_PROJECT,
        resource_path="config_path",
        suites=[],
        output_folder="test",
    )
    suite = TestSuite(name="my_test_suite", tests=[])
    test = Test(
        "test_name",
        "test_command",
        variables={"variable1": "{{variable2}}", "variable2": "{{variable1}}"},
        comparison_settings=ComparisonSettings.default(),
    )
    variable_processor = VariableProcessor()

    with pytest.raises(VariableSubstitutionRecursionDepthExceeded):
        variable_processor.evaluate_variables(config, suite, test)
