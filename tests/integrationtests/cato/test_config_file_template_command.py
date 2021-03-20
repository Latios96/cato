import json
import os

from pytest_bdd import scenario, given, when, then

from cato.config.config_template_generator import TEMPLATE
from tests.integrationtests.command_fixture import run_cato_command


@scenario(
    "test_config_file_template_command.feature",
    "Create a new cato.json in an empty folder",
)
def test_in_empty_folder(scenario_context):
    assert scenario_context["command_result"].output_contains_line(
        "[INFO]  Wrote config file to {}".format(scenario_context["config_path"])
    )


@scenario(
    "test_config_file_template_command.feature",
    "Create a cato.json in a folder with an existing cato.json",
)
def test_in_non_emptyfolder(scenario_context):
    assert scenario_context["command_result"].output_contains_line(
        "[INFO]  Wrote config file to {}".format(scenario_context["config_path"])
    )


@given("An empty folder")
def step_impl(scenario_context, tmp_path):
    scenario_context["config_folder"] = str(tmp_path)
    scenario_context["config_path"] = os.path.join(str(tmp_path), "cato.json")
    assert os.listdir(str(tmp_path)) == []


@then("a new cato.json should be created based on template")
def step_impl(scenario_context):
    assert os.listdir(scenario_context["config_folder"]) == ["cato.json"]


@when("I run the config-template command with the folder")
def step_impl(scenario_context):
    command_result = run_cato_command(
        ["config-template", scenario_context["config_folder"]]
    )
    assert command_result.exit_code == 0
    scenario_context["command_result"] = command_result


@given("a folder with non default cato.json")
def step_impl(scenario_context, tmp_path):
    config_folder = str(tmp_path)
    scenario_context["config_folder"] = config_folder
    scenario_context["config_path"] = os.path.join(str(tmp_path), "cato.json")
    with open(scenario_context["config_path"], "w") as f:
        f.write("Hello world")


@then("the cato.json should be overriden with template")
def step_impl(scenario_context):
    with open(scenario_context["config_path"]) as f:
        content = json.load(f)

    assert content == TEMPLATE
