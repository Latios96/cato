import hashlib
import os
import shutil

import pytest
from PIL import Image
from checksumdir import dirhash
from pytest_bdd import scenario, given, when, then

from tests.integrationtests.command_fixture import run_cato_command


@scenario(
    "test_update_reference_image.feature",
    "Updating reference image which did not exist before",
)
def test_in_folder():
    pass


@scenario(
    "test_update_reference_image.feature",
    "Updating reference image which did exist before",
)
def test_in_folder():
    pass


@scenario(
    "test_update_reference_image.feature",
    "Updating reference to a not existing output file fails",
)
def test_in_folder():
    pass


@pytest.fixture
def cato_config(tmp_path, test_resource_provider, scenario_context):
    config_folder = os.path.join(str(tmp_path), "config_folder")
    shutil.copytree(
        test_resource_provider.resource_by_name("cato_cmd_integ_tests"), config_folder
    )

    scenario_context["config_folder"] = config_folder
    scenario_context["config_path"] = os.path.join(config_folder, "cato.json")


@given("a cato.json file with tests")
def step_impl(cato_config):
    pass


def write_image(path, color=None):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    img = Image.new("RGB", (800, 600), (255, 255, 255) if not color else color)
    img.save(path, "PNG")


def hash_file(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


@given("an output image for a test")
def step_impl(scenario_context):
    image_path = os.path.join(
        scenario_context["config_folder"],
        "result",
        "WriteImages",
        "write_white_image",
        "write_white_image.png",
    )
    write_image(image_path)
    scenario_context["output_image"] = image_path
    scenario_context["output_image_checksum"] = hash_file(image_path)


@given("reference images for other tests")
def step_impl(scenario_context):
    reference_image_folder = os.path.join(
        scenario_context["config_folder"], "WriteImages"
    )
    image_path = os.path.join(
        reference_image_folder,
        "write_black_image",
        "write_black_image.png",
    )

    write_image(image_path, (0, 0, 0))

    scenario_context["other_tests_reference_image"] = image_path
    scenario_context["other_tests_reference_checksum"] = hash_file(image_path)
    scenario_context["reference_image_folder"] = reference_image_folder
    scenario_context["reference_dir_checksum"] = dirhash(reference_image_folder, "md5")


@given("a reference image exists for the test")
def step_impl(scenario_context):
    image_path = os.path.join(
        scenario_context["config_folder"],
        "WriteImages",
        "write_white_image",
        "write_white_image.png",
    )

    write_image(image_path, (1, 1, 1))

    scenario_context["test_reference_image"] = image_path
    scenario_context["test_reference_checksum"] = hash_file(image_path)


@when("I run the update reference image command")
def step_impl(scenario_context, dir_changer):
    os.chdir(scenario_context["config_folder"])

    command_result = run_cato_command(
        ["update-reference", "--test-identifier", "WriteImages/write_white_image"]
    )

    assert command_result.exit_code == 0


@when("I run the update reference image command for a not existing test")
def step_impl(scenario_context, dir_changer):
    os.chdir(scenario_context["config_folder"])

    command_result = run_cato_command(
        ["update-reference", "--test-identifier", "WriteImages/NOT_EXISTING"]
    )


@then("the output image should be stored as reference image")
def step_impl(scenario_context):
    reference_image_path = os.path.join(
        scenario_context["config_folder"],
        "result",
        "WriteImages",
        "write_white_image",
        "write_white_image.png",
    )

    assert os.path.exists(reference_image_path)

    reference_image_checksum = hash_file(reference_image_path)
    assert scenario_context["output_image_checksum"] == reference_image_checksum


@then("other reference images should be untouched")
def step_impl(scenario_context):
    assert (
        hash_file(scenario_context["other_tests_reference_image"])
        == scenario_context["other_tests_reference_checksum"]
    )


@then("all reference images should be untouched")
def step_impl(scenario_context):
    assert scenario_context["reference_dir_checksum"] == dirhash(
        scenario_context["reference_image_folder"], "md5"
    )
