import os

from tests.integrationtests.command_fixture import run_cato_command


def test_list_tests_described_in_a_config_file(test_resource_provider):
    config_folder = test_resource_provider.resource_by_name("cato_test_config")
    os.chdir(config_folder)
    result = run_the_list_tests_command()
    assert_result_contains_test_identifiers(result)


def test_list_tests_described_in_a_config_file_from_current_dir(test_resource_provider):
    config_folder = test_resource_provider.resource_by_name("cato_test_config")
    result = run_the_list_tests_command_with_path_to_config(config_folder)
    assert_result_contains_test_identifiers(result)


def run_the_list_tests_command():
    command_result = run_cato_command(["list-tests"])
    assert command_result.exit_code == 0
    return command_result


def assert_result_contains_test_identifiers(command_result):
    assert command_result.output_contains_line(
        "[INFO]  My_first_test_Suite/My_first_test"
    )


def run_the_list_tests_command_with_path_to_config(config_folder):
    config_path = os.path.join(config_folder, "cato.json")
    command_result = run_cato_command(["list-tests", "--path", config_path])
    assert command_result.exit_code == 0
    return command_result


def assert_result_contains_test_identifiers(command_result):
    assert command_result.output_contains_line(
        "[INFO]  My_first_test_Suite/My_first_test"
    )
