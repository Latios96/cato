import datetime

import pytest

from cato_server.api.schemas.test_result_schemas import CreateTestResultSchema


class TestCreateTestResultSchema:
    def test_success_with_required_fields_only(self):
        schema = CreateTestResultSchema()
        data = {
            "suite_result_id": 1,
            "test_name": "my_test_name",
            "test_identifier": "my_suite/test_identifier",
            "test_command": "my_command",
            "test_variables": {"key": "value"},
            "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
            "execution_status": "NOT_STARTED",
        }

        errors = schema.validate(data)

        assert errors == {}

    def test_success_with_all_fields(self):
        schema = CreateTestResultSchema()
        data = {
            "suite_result_id": 1,
            "test_name": "my_test_name",
            "test_identifier": "my_suite/test_identifier",
            "test_command": "my_command",
            "test_variables": {"key": "value"},
            "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
            "execution_status": "NOT_STARTED",
            "status": "SUCCESS",
            "output": ["1", "2", "3"],
            "seconds": 5,
            "message": "my_message",
            "image_output": 1,
            "reference_image": 2,
            "started_at": datetime.datetime.now().isoformat(),
            "finished_at": datetime.datetime.now().isoformat(),
        }

        errors = schema.validate(data)

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "suite_result_id": ["Missing data for required field."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": ["Missing data for required field."],
                    "test_name": ["Missing data for required field."],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {"suite_result_id": "wurst"},
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "suite_result_id": ["Not a valid integer."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": ["Missing data for required field."],
                    "test_name": ["Missing data for required field."],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {"suite_result_id": 1, "test_name": "$!"},
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": ["Missing data for required field."],
                    "test_name": ["String does not match expected pattern."],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "wurst",
                },
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": [
                        'String "wurst" is not a valid TestIdentifier.'
                    ],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "",
                },
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "test_command": ["Shorter than minimum length 1."],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "my_command",
                    "test_variables": {"key": ["val", "ue"]},
                },
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                    "test_variables": ["Not a mapping of str->str: key=['val', 'ue']"],
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "test_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {},
                },
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": {
                        "cores": ["Missing data for required field."],
                        "cpu_name": ["Missing data for required field."],
                        "memory": ["Missing data for required field."],
                    },
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "test_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cores": 8},
                },
                {
                    "execution_status": ["Missing data for required field."],
                    "machine_info": {
                        "cpu_name": ["Missing data for required field."],
                        "memory": ["Missing data for required field."],
                    },
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "test_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {
                        "cores": 8,
                        "memory": 24,
                        "cpu_name": "Intel Xeon",
                    },
                },
                {
                    "execution_status": ["Missing data for required field."],
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "test_name",
                    "test_identifier": "my_suite/test_name",
                    "test_command": "test_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {
                        "cores": 8,
                        "memory": 24,
                        "cpu_name": "Intel Xeon",
                    },
                    "execution_status": "wurst",
                },
                {
                    "execution_status": ["Invalid enum member wurst"],
                },
            ),
        ],
    )
    def test_failure_required_fields(self, data, expected_errors):
        schema = CreateTestResultSchema()

        errors = schema.validate(data)

        assert errors == expected_errors

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "test",
                },
                {"status": ["Invalid enum member test"]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": [1, 2, 3],
                },
                {
                    "output": {
                        0: ["Not a valid string."],
                        1: ["Not a valid string."],
                        2: ["Not a valid string."],
                    }
                },
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "five",
                },
                {"seconds": ["Not a valid number."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": 5,
                    "message": 5,
                },
                {"message": ["Not a valid string."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "5",
                    "image_output": "random",
                },
                {"image_output": ["Not a valid integer."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "5",
                    "image_output": 1,
                    "reference_image": "sdfsdf2",
                },
                {"reference_image": ["Not a valid integer."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "5",
                    "image_output": 1,
                    "reference_image": 2,
                    "started_at": "yesterday",
                },
                {"started_at": ["Not a valid datetime."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "5",
                    "image_output": 1,
                    "reference_image": 2,
                    "started_at": datetime.datetime.now().isoformat(),
                    "finished_at": "tomorrow",
                },
                {"finished_at": ["Not a valid datetime."]},
            ),
            (
                {
                    "suite_result_id": 1,
                    "test_name": "my_test_name",
                    "test_identifier": "my_suite/test_identifier",
                    "test_command": "my_command",
                    "test_variables": {"key": "value"},
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                    "execution_status": "NOT_STARTED",
                    "status": "SUCCESS",
                    "output": ["1", "2", "3"],
                    "seconds": "5",
                    "image_output": 1,
                    "reference_image": 2,
                    "started_at": datetime.datetime.now().isoformat(),
                    "finished_at": datetime.datetime.now().isoformat(),
                },
                {},
            ),
        ],
    )
    def test_failure_optional_fields(self, data, expected_errors):
        schema = CreateTestResultSchema()

        errors = schema.validate(data)

        assert errors == expected_errors
