import os

import pytest
from pytest_bdd import scenario, given, when, then

from tests.integrationtests.command_fixture import run_cato_command


@pytest.fixture
def scenario_context():
    return {}


@pytest.fixture
def dir_changer():
    old_dir = os.getcwd()
    yield
    os.chdir(old_dir)


@scenario("test_list_tests_command.feature", "In Folder with cato.json")
def test_in_folder():
    pass


@scenario("test_list_tests_command.feature", "Path to config")
def test_path_to_config():
    pass


@given("I run the list-tests command")
def step_impl(scenario_context):
    command_result = run_cato_command(["list-tests"])
    assert command_result.exit_code == 0
    scenario_context["command_result"] = command_result


@then("I should see the test identifiers of the config on the terminal")
def step_impl(scenario_context):
    assert scenario_context["command_result"].output_contains_line(
        "[INFO]  My_first_test_Suite/My_first_test"
    )


@given("A folder with a valid cato.json")
def step_impl(scenario_context, test_resource_provider):
    scenario_context["config_folder"] = test_resource_provider.resource_by_name(
        "cato_test_config"
    )


@given("I change to this folder")
def step_impl(scenario_context, dir_changer):
    os.chdir(scenario_context["config_folder"])


@given("I run the list-tests command with the path to the config")
def step_impl(scenario_context):
    config_path = os.path.join(scenario_context["config_folder"], "cato.json")
    scenario_context["command_result"] = run_cato_command(
        ["list-tests", "--path", config_path]
    )
