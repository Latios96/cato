import os
import sys

import requests
from pytest_bdd import scenario, given, when, then

from tests.integrationtests.command_fixture import run_cato_command, run_command


@scenario(
    "test_run_command.feature",
    "Run all tests the first time should fail because of missing reference images",
)
def test_all_test_failing_not_existing_reference_images():
    pass


@scenario(
    "test_run_command.feature",
    "Run all tests should succeed",
)
def test_all_test_succeed():
    pass


@given("a cato.json file with tests")
def step_impl(cato_config):
    pass


@when("I run the run command")
def step_impl(scenario_context, dir_changer, live_server):
    os.chdir(scenario_context["config_folder"])

    result = run_cato_command(["run", "-u", live_server.server_url(), "-vvv"])
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
    assert scenario_context["command_result"].output_contains_line_matching("2  failed")


@then("Failure Messages for missing reference image should be printed")
def step_impl(scenario_context):
    assert scenario_context["command_result"].output_contains_line_matching(
        "write_white_image failed .*: Reference image <not found> does not exist!"
    )
    assert scenario_context["command_result"].output_contains_line_matching(
        "write_black_image failed .*: Reference image <not found> does not exist!"
    )


@then("the result should be available at the server")
def step_impl(live_server, scenario_context):
    run_id = _parse_run_id_from_output(scenario_context)
    run_json = _read_run_from_server(live_server, run_id)
    assert run_json == [
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


@given("reference images exist for the tests")
def step_impl(scenario_context):
    cato_cmd = [
        sys.executable,
        os.path.join(scenario_context["config_folder"], "WriteImages", "write.py"),
        os.path.join(
            scenario_context["config_folder"],
            "WriteImages",
            "write_white_image",
            "reference.png",
        ),
        "white",
    ]
    result = run_command(cato_cmd)
    assert result.exit_code == 0

    cato_cmd = [
        sys.executable,
        os.path.join(scenario_context["config_folder"], "WriteImages", "write.py"),
        os.path.join(
            scenario_context["config_folder"],
            "WriteImages",
            "write_black_image",
            "reference.png",
        ),
        "black",
    ]
    result = run_command(cato_cmd)
    assert result.exit_code == 0


@then("no failure message should be printed")
def step_impl(scenario_context):
    assert not scenario_context["command_result"].output_contains_line_matching(
        ".* failed"
    )


@then("a success message should be printed")
def step_impl(scenario_context):
    assert not scenario_context["command_result"].output_contains_line("2 succeded ✅")


@then("the success result should be available at the server")
def step_impl(scenario_context, live_server):
    run_id = _parse_run_id_from_output(scenario_context)
    run_json = _read_run_from_server(live_server, run_id)
    assert run_json == [
        {
            "execution_status": "FINISHED",
            "id": 2,
            "name": "write_black_image",
            "status": "SUCCESS",
            "test_identifier": "WriteImages/write_black_image",
        },
        {
            "execution_status": "FINISHED",
            "id": 1,
            "name": "write_white_image",
            "status": "SUCCESS",
            "test_identifier": "WriteImages/write_white_image",
        },
    ]


def _read_run_from_server(live_server, run_id):
    url = live_server.server_url() + "/api/v1/test_results/run/" + run_id
    response = requests.get(url)
    assert response.status_code == 200
    json = response.json()
    return json


def _parse_run_id_from_output(scenario_context):
    match = scenario_context["command_result"].output_contains_line_matching(
        "You can find your run at http://127.0.0.1:\d+/#/projects/\d+/runs/(\d+)"
    )
    assert match
    run_id = match.group(1)
    return run_id
