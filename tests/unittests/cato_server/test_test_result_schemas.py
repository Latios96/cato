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

        errors = schema.validate({"testResultId": 1, "text": "This is a long text"})

        assert errors == {}

    def test_success_max_length_string(self):
        schema = CreateOutputSchema()

        errors = schema.validate({"testResultId": 1, "text": STRING_WITH_MAX_SIZE})

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "testResultId": ["Missing data for required field."],
                    "text": ["Missing data for required field."],
                },
            ),
            (
                {"testResultId": "wurst", "text": "This is a long text"},
                {"testResultId": ["Not a valid integer."]},
            ),
            (
                {"testResultId": 1, "text": ["This is a long text"]},
                {"text": ["Not a valid string."]},
            ),
            (
                {"testResultId": 1, "text": STRING_WITH_MAX_SIZE + "x"},
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
            {"id": 42, "machineInfo": {"cpuName": "Intel", "cores": 8, "memory": 24}}
        )

        assert errors == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {},
                {
                    "id": ["Missing data for required field."],
                    "machineInfo": ["Missing data for required field."],
                },
            ),
            (
                {
                    "id": "w",
                    "machineInfo": {"cpuName": "Intel", "cores": 8, "memory": 24},
                },
                {"id": ["Not a valid integer."]},
            ),
            (
                {
                    "id": 42,
                    "machineInfo": {"cpu_wname": "Intel", "cores": 8, "memory": 24},
                },
                {"machineInfo": {"cpuName": ["Missing data for required field."]}},
            ),
            (
                {
                    "id": 42,
                    "machineInfo": {
                        "cpuName": "Intel",
                        "cores": "eight",
                        "memory": 24,
                    },
                },
                {"machineInfo": {"cores": ["Not a valid integer."]}},
            ),
            (
                {
                    "id": 42,
                    "machineInfo": {"cpuName": "Intel", "cores": -8, "memory": -24},
                },
                {
                    "machineInfo": {
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
