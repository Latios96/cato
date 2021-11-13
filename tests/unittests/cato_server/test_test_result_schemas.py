import humanfriendly
import pytest

from cato_server.api.schemas.test_result_schemas import (
    CreateOutputSchema,
    StartTestResultSchema,
)

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
