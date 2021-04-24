import datetime

import humanfriendly
import pytest

from cato_server.api.schemas.test_result_schemas import (
    CreateTestResultSchema,
    CreateOutputSchema,
    StartTestResultSchema,
)


class TestCreateTestResultSchema:
    def test_success_with_required_fields_only(self):
        schema = CreateTestResultSchema()
        data = {
            "suite_result_id": 1,
            "test_name": "my_test_name",
            "test_identifier": "my_suite/test_identifier",
            "test_command": "my_command",
            "test_variables": {"key": "value"},
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
                    "suite_result_id": ["Not a valid integer."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": ["Missing data for required field."],
                    "test_name": ["Missing data for required field."],
                    "test_variables": ["Missing data for required field."],
                },
            ),
            (
                {"suite_result_id": 1, "test_name": ":"},
                {
                    "execution_status": ["Missing data for required field."],
                    "test_command": ["Missing data for required field."],
                    "test_identifier": ["Missing data for required field."],
                    "test_name": [
                        "':' is a reserved name, reason=RESERVED_NAME, target-platform=universal, reusable_name=False"
                    ],
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


STRING_WITH_MAX_SIZE = "".join(["x" for x in range(humanfriendly.parse_size("10mb"))])


class TestCreateOutputSchema:
    def test_success(self):
        schema = CreateOutputSchema()

        errors = schema.validate({"test_result_id": 1, "text": "This is a long text"})

        assert errors == {}

    def test_success_max_length_string(self):
        schema = CreateOutputSchema()

        errors = schema.validate({"test_result_id": 1, "text": STRING_WITH_MAX_SIZE})

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "test_result_id": ["Missing data for required field."],
                    "text": ["Missing data for required field."],
                },
            ),
            (
                {"test_result_id": "wurst", "text": "This is a long text"},
                {"test_result_id": ["Not a valid integer."]},
            ),
            (
                {"test_result_id": 1, "text": ["This is a long text"]},
                {"text": ["Not a valid string."]},
            ),
            (
                {"test_result_id": 1, "text": STRING_WITH_MAX_SIZE + "x"},
                {"text": ["Longer than maximum length 10000000."]},
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        schema = CreateOutputSchema()

        errors = schema.validate(data)

        assert errors == expected_errors


class TestStartTestResultSchema:
    def test_success(self):
        schema = StartTestResultSchema()

        errors = schema.validate(
            {"id": 42, "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24}}
        )

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "id": ["Missing data for required field."],
                    "machine_info": ["Missing data for required field."],
                },
            ),
            (
                {
                    "id": "w",
                    "machine_info": {"cpu_name": "Intel", "cores": 8, "memory": 24},
                },
                {"id": ["Not a valid integer."]},
            ),
            (
                {
                    "id": 42,
                    "machine_info": {"cpu_wname": "Intel", "cores": 8, "memory": 24},
                },
                {"machine_info": {"cpu_name": ["Missing data for required field."]}},
            ),
            (
                {
                    "id": 42,
                    "machine_info": {
                        "cpu_name": "Intel",
                        "cores": "eight",
                        "memory": 24,
                    },
                },
                {"machine_info": {"cores": ["Not a valid integer."]}},
            ),
            (
                {
                    "id": 42,
                    "machine_info": {"cpu_name": "Intel", "cores": -8, "memory": -24},
                },
                {
                    "machine_info": {
                        "cores": ["Must be greater than or equal to 1."],
                        "memory": ["Must be greater than or equal to 0."],
                    }
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        schema = StartTestResultSchema()

        errors = schema.validate(data)

        assert errors == expected_errors
