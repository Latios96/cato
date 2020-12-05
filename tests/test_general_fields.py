import pytest
from marshmallow import Schema

from cato_server.api.schemas.general import ID_FIELD, NAME_FIELD, VARIABLES_FIELD


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
        (NAME_FIELD, "$my_name", ["String does not match expected pattern."]),
        (NAME_FIELD, "my/name", ["String does not match expected pattern."]),
        (VARIABLES_FIELD, [], ["Not a valid mapping type."]),
        (
            VARIABLES_FIELD,
            {"key": ["val", "ue"]},
            ["Not a mapping of str->str: key=['val', 'ue']"],
        ),
    ],
)
def test_field_failure(field, value, expected_errors):
    class TestSchema(Schema):
        field_to_test = field

    errors = TestSchema().validate({"field_to_test": value})

    assert errors == {"field_to_test": expected_errors}
