import os

import requests
from pytest_bdd import scenario, given, when, then

from tests.integrationtests.command_fixture import run_cato_command


@scenario(
    "test_run_command.feature",
    "Run all tests the first time should fail because of missing reference images",
)
def test_update_not_existing():
    pass


@given("a cato.json file with tests")
def step_impl(cato_config):
    pass


@when("I run the run command")
def step_impl(scenario_context, dir_changer, live_server):
    os.chdir(scenario_context["config_folder"])

    result = run_cato_command(["run", "-u", live_server.server_url(), "-v"])
    scenario_context["command_result"] = result

    assert result.exit_code == 0


@given("no reference images for the tests")
def step_impl():
    pass


@then("All tests should have been executed")
def step_impl(scenario_context):
    assert scenario_context["command_result"].output_contains_line("Ran 2 tests")


@then("A failure message should be printed")
def step_impl(scenario_context):
    assert scenario_context["command_result"].output_contains_line("2  failed   ❌")


@then("Failure Messages for missing reference image should be printed")
def step_impl(scenario_context):
    assert scenario_context["command_result"].output_contains_line_matching(
        "write_white_image failed ❌: Reference image <not found> does not exist!"
    )
    assert scenario_context["command_result"].output_contains_line_matching(
        "write_black_image failed ❌: Reference image <not found> does not exist!"
    )


@then("the result should be available at the server")
def step_impl(live_server, scenario_context):
    match = scenario_context["command_result"].output_contains_line_matching(
        "You can find your run at http://127.0.0.1:\d+/#/projects/\d+/runs/(\d+)"
    )
    assert match
    run_id = match.group(1)
    url = live_server.server_url() + "/api/v1/test_results/run/" + run_id
    response = requests.get(url)
    assert response.status_code == 200
    assert response.json() == [
        {
            "execution_status": "FINISHED",
            "id": 2,
            "name": "write_black_image",
            "status": "FAILED",
            "test_identifier": "WriteImages/write_black_image",
        },
        {
            "execution_status": "FINISHED",
            "id": 1,
            "name": "write_white_image",
            "status": "FAILED",
            "test_identifier": "WriteImages/write_white_image",
        },
    ]
