import json
import os

import pytest

from cato.config.config_template_generator import TEMPLATE
from tests.integrationtests.command_fixture import run_cato_command


@pytest.fixture
def empty_folder(tmp_path):
    config_folder = str(tmp_path)
    config_path = os.path.join(str(tmp_path), "cato.json")
    return config_folder, config_path


def test_create_a_new_cato_json_in_an_empty_folder(empty_folder):
    config_folder, config_path = empty_folder

    run_config_template_command_in_folder(config_folder)

    assert_config_folder_contains_cato_json(config_folder)


def test_create_a_cato_json_in_a_non_empty_folder_should_override(empty_folder):
    config_folder, config_path = empty_folder
    write_non_default_cato_json(config_path)

    run_config_template_command_in_folder(config_folder)

    assert_config_folder_contains_template_cato_json(config_path)


def write_non_default_cato_json(config_folder):
    with open(config_folder, "w") as f:
        f.write("Hello world")


def run_config_template_command_in_folder(config_folder):
    command_result = run_cato_command(["config-template", config_folder])
    assert command_result.exit_code == 0


def assert_config_folder_contains_cato_json(config_folder):
    assert os.listdir(config_folder) == ["cato.json"]


def assert_config_folder_contains_template_cato_json(config_path):
    with open(config_path) as f:
        content = json.load(f)

    assert content == TEMPLATE
