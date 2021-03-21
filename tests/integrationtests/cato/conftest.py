import os
import shutil

import pytest


@pytest.fixture
def scenario_context():
    return {}


@pytest.fixture
def dir_changer():
    old_dir = os.getcwd()
    yield
    os.chdir(old_dir)


@pytest.fixture
def cato_config(tmp_path, test_resource_provider, scenario_context):
    config_folder = os.path.join(str(tmp_path), "config_folder")
    shutil.copytree(
        test_resource_provider.resource_by_name("cato_cmd_integ_tests"), config_folder
    )

    scenario_context["config_folder"] = config_folder
    scenario_context["config_path"] = os.path.join(config_folder, "cato.json")


@pytest.fixture
def create_result_path(scenario_context):
    def f(suite_name, test_name):
        return os.path.join(
            scenario_context["config_folder"],
            "result",
            suite_name,
            test_name,
            test_name + ".png",
        )

    return f


@pytest.fixture
def create_reference_path(scenario_context):
    def f(suite_name, test_name):
        return os.path.join(
            scenario_context["config_folder"], suite_name, test_name, "reference.png"
        )

    return f
