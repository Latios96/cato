import pytest
from marshmallow import Schema

from cato_server.api.schemas.general import (
    ID_FIELD,
    NAME_FIELD,
    VARIABLES_FIELD,
    MachineInfoSchema,
    FILE_PATH_FIELD,
    OPTIONAL_VARIABLES_FIELD,
)


@pytest.mark.parametrize(
    "field,value",
    [
        (ID_FIELD, 1),
        (NAME_FIELD, "my_name"),
        (NAME_FIELD, "my-name"),
        (NAME_FIELD, "my-name22"),
        (NAME_FIELD, "22"),
        (VARIABLES_FIELD, {}),
        (VARIABLES_FIELD, {"key": "value"}),
        (OPTIONAL_VARIABLES_FIELD, {}),
        (OPTIONAL_VARIABLES_FIELD, {"key": "value"}),
        (FILE_PATH_FIELD, "my-name22"),
    ],
)
def test_field_success(field, value):
    class TestSchema(Schema):
        field_to_test = field

    errors = TestSchema().validate({"field_to_test": value})

    assert errors == {}


@pytest.mark.parametrize(
    "field,value,expected_errors",
    [
        (ID_FIELD, "tesetset", ["Not a valid integer."]),
        (ID_FIELD, -1, ["Must be greater than or equal to 0."]),
        (
            NAME_FIELD,
            ":my_name",
            [
                "invalid char found: invalids=(':'), value=':my_name', reason=INVALID_CHARACTER, target-platform=Windows"
            ],
        ),
        (
            NAME_FIELD,
            "my/name",
            [
                "invalid char found: invalids=('/'), value='my/name', reason=INVALID_CHARACTER, target-platform=Windows"
            ],
        ),
        (VARIABLES_FIELD, [], ["Not a valid mapping type."]),
        (OPTIONAL_VARIABLES_FIELD, [], ["Not a valid mapping type."]),
        (
            VARIABLES_FIELD,
            {"key": ["val", "ue"]},
            ["Not a mapping of str->str: key=['val', 'ue']"],
        ),
        (
            FILE_PATH_FIELD,
            "my|name",
            [
                "invalid char found: invalids=('|'), value='my|name', reason=INVALID_CHARACTER, target-platform=Windows"
            ],
        ),
    ],
)
def test_field_failure(field, value, expected_errors):
    class TestSchema(Schema):
        field_to_test = field

    errors = TestSchema().validate({"field_to_test": value})

    assert errors == {"field_to_test": expected_errors}


class TestMaschineInfoSchema:
    def test_success(self):
        schema = MachineInfoSchema()

        result = schema.validate({"cpu_name": "name", "cores": 8, "memory": 1})

        assert result == {}

    @pytest.mark.parametrize(
        "data,expected_errors",
        [
            (
                {"cores": 8, "memory": 1},
                {"cpu_name": ["Missing data for required field."]},
            ),
            (
                {"cpu_name": "name", "cores": -1, "memory": 1},
                {"cores": ["Must be greater than or equal to 1."]},
            ),
            (
                {"cpu_name": "name", "cores": -1, "memory": -1},
                {
                    "cores": ["Must be greater than or equal to 1."],
                    "memory": ["Must be greater than or equal to 0."],
                },
            ),
        ],
    )
    def test_failure(self, data, expected_errors):
        schema = MachineInfoSchema()

        result = schema.validate(data)

        assert result == expected_errors
