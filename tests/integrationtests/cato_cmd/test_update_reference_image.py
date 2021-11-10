import hashlib
import os

from PIL import Image
from checksumdir import dirhash
from pytest_bdd import scenario, given, when, then

from tests.integrationtests.command_fixture import run_cato_command


def test_updating_reference_image_which_did_not_exist_before(cato_config):
    output_image_path, output_image_hash = ensure_image_output_for_a_test(cato_config)
    run_update_reference_image_command(cato_config)
    assert_output_image_should_be_stored_as_reference_image(
        cato_config, output_image_hash
    )


def test_updating_missing_reference_images(cato_config):
    output_image_path, output_image_hash = ensure_image_output_for_a_test(cato_config)
    ensure_reference_image_for_other_test(cato_config)
    run_update_missing_reference_image_command(cato_config)
    ensure_output_image_is_stored_as_reference_image(cato_config, output_image_hash)


def run_update_reference_image_command(cato_config):
    config_folder, config_path = cato_config
    os.chdir(config_folder)

    command_result = run_cato_command(
        ["update-reference", "--test-identifier", "WriteImages/write_white_image"]
    )

    assert command_result.exit_code == 0


def ensure_image_output_for_a_test(cato_config):
    image_path = create_result_path(cato_config, "WriteImages", "write_white_image")
    write_image(image_path)
    return image_path, hash_file(image_path)


def create_result_path(cato_config, suite_name, test_name):
    config_folder, config_path = cato_config
    return os.path.join(
        config_folder,
        "result",
        suite_name,
        test_name,
        test_name + ".png",
    )


def ensure_reference_image_for_other_test(cato_config):
    config_folder, config_path = cato_config
    reference_image_folder = os.path.join(config_folder, "WriteImages")

    image_path = create_reference_path(cato_config, "WriteImages", "write_black_image")
    write_image(image_path, (0, 0, 0))

    other_tests_reference_image = image_path
    other_tests_reference_checksum = hash_file(image_path)
    reference_image_folder = reference_image_folder
    reference_dir_checksum = hash_directory(reference_image_folder)


def create_reference_path(cato_config, suite_name, test_name):
    config_folder, config_path = cato_config

    return os.path.join(config_folder, suite_name, test_name, "reference.png")


def assert_output_image_should_be_stored_as_reference_image(
    cato_config, output_image_checksum
):
    reference_image_path = create_reference_path(
        cato_config, "WriteImages", "write_white_image"
    )

    assert os.path.exists(reference_image_path)

    reference_image_checksum = hash_file(reference_image_path)
    assert output_image_checksum == reference_image_checksum


def run_update_missing_reference_image_command(cato_config):
    config_folder, config_path = cato_config
    os.chdir(config_folder)

    command_result = run_cato_command(
        [
            "update-missing-reference-images",
        ]
    )

    assert command_result.exit_code == 0


def ensure_output_image_is_stored_as_reference_image(
    cato_config, output_image_checksum
):
    reference_image_path = create_reference_path(
        cato_config, "WriteImages", "write_white_image"
    )

    assert os.path.exists(reference_image_path)

    reference_image_checksum = hash_file(reference_image_path)
    assert output_image_checksum == reference_image_checksum


def write_image(path, color=None):
    folder = os.path.dirname(path)
    if not os.path.exists(folder):
        os.makedirs(folder)
    img = Image.new("RGB", (800, 600), (255, 255, 255) if not color else color)
    img.save(path, "PNG")


def hash_file(path):
    return hashlib.md5(open(path, "rb").read()).hexdigest()


def hash_directory(path):
    return dirhash(path, "md5")
