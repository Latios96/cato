import os
import sys

import requests

from tests.integrationtests.command_fixture import run_cato_command, run_command


def test_run_tests_fails_because_of_missing_reference_images(
    cato_config, live_server, env_with_api_token, api_token_str
):
    result = run_the_cato_command(live_server, cato_config, env_with_api_token)
    assert_all_tests_should_have_been_executed(result)
    assert_a_failure_message_was_printed(result)
    assert_a_failure_message_for_missing_reference_image_was_printed(result)
    assert_the_failure_result_is_available_on_the_server(
        result, live_server, api_token_str
    )


def test_running_all_tests_should_succeed(
    cato_config, live_server, env_with_api_token, api_token_str
):
    reference_images_exist(cato_config, env_with_api_token)
    result = run_the_cato_command(live_server, cato_config, env_with_api_token)
    assert_all_tests_should_have_been_executed(result)
    assert_no_failure_message_was_printed(result)
    assert_success_message_was_printed(result)
    assert_the_success_result_is_available_on_the_server(
        result, live_server, api_token_str
    )


def run_the_cato_command(live_server, cato_config, env_with_api_token):
    config_folder, config_path = cato_config
    os.chdir(config_folder)
    result = run_cato_command(
        ["run", "-u", live_server.server_url(), "-vvv"], env_with_api_token
    )
    assert result.exit_code == 0
    return result


def assert_all_tests_should_have_been_executed(command_result):
    assert command_result.output_contains_line("Ran 2 tests")


def assert_a_failure_message_was_printed(command_result):
    assert command_result.output_contains_line_matching("2  failed")


def assert_a_failure_message_for_missing_reference_image_was_printed(command_result):
    assert command_result.output_contains_line_matching(
        "write_white_image failed .*: Reference image <not found> does not exist!"
    )
    assert command_result.output_contains_line_matching(
        "write_black_image failed .*: Reference image <not found> does not exist!"
    )


def assert_the_failure_result_is_available_on_the_server(
    command_result, live_server, api_token_str
):
    run_id = _parse_run_id_from_output(command_result)
    run_json = _read_run_from_server(live_server, run_id, api_token_str)
    assert run_json == [
        {
            "unifiedTestStatus": "FAILED",
            "id": 2,
            "name": "write_black_image",
            "testIdentifier": "WriteImages/write_black_image",
            "thumbnailFileId": None,
        },
        {
            "unifiedTestStatus": "FAILED",
            "id": 1,
            "name": "write_white_image",
            "testIdentifier": "WriteImages/write_white_image",
            "thumbnailFileId": None,
        },
    ]


def reference_images_exist(cato_config, env_with_api_token):
    config_folder, config_path = cato_config
    cato_cmd = [
        sys.executable,
        os.path.join(config_folder, "WriteImages", "write.py"),
        os.path.join(
            config_folder,
            "WriteImages",
            "write_white_image",
            "reference.png",
        ),
        "white",
    ]
    result = run_command(cato_cmd, env_with_api_token)
    assert result.exit_code == 0

    cato_cmd = [
        sys.executable,
        os.path.join(config_folder, "WriteImages", "write.py"),
        os.path.join(
            config_folder,
            "WriteImages",
            "write_black_image",
            "reference.png",
        ),
        "black",
    ]
    result = run_command(cato_cmd, env_with_api_token)
    assert result.exit_code == 0


def assert_no_failure_message_was_printed(command_result):
    assert not command_result.output_contains_line_matching(".* failed")


def assert_success_message_was_printed(command_result):
    assert not command_result.output_contains_line("2 succeded ✅")


def assert_the_success_result_is_available_on_the_server(
    command_result, live_server, api_token_str
):
    run_id = _parse_run_id_from_output(command_result)
    run_json = _read_run_from_server(live_server, run_id, api_token_str)
    assert run_json == [
        {
            "unifiedTestStatus": "SUCCESS",
            "id": 2,
            "name": "write_black_image",
            "testIdentifier": "WriteImages/write_black_image",
            "thumbnailFileId": None,
        },
        {
            "unifiedTestStatus": "SUCCESS",
            "id": 1,
            "name": "write_white_image",
            "testIdentifier": "WriteImages/write_white_image",
            "thumbnailFileId": None,
        },
    ]


def _read_run_from_server(live_server, run_id, api_token_str):
    url = live_server.server_url() + "/api/v1/test_results/run/" + run_id
    response = requests.get(
        url, headers={"Authorization": str(api_token_str.to_bearer())}
    )
    assert response.status_code == 200
    json = response.json()
    return json


def _parse_run_id_from_output(command_result):
    match = command_result.output_contains_line_matching(
        "You can find your run at http://127.0.0.1:\d+/projects/\d+/runs/(\d+)"
    )
    assert match
    run_id = match.group(1)
    return run_id
