from cato_server.domain.suite_result import SuiteResult
from cato_server.mappers.internal.suite_result_class_mapper import (
    SuiteResultClassMapper,
)


def test_map_from_dict():
    mapper = SuiteResultClassMapper()

    result = mapper.map_from_dict(
        {
            "id": 1,
            "run_id": 1,
            "suite_name": "suite_name",
            "suite_variables": {"key": "value"},
        }
    )

    assert result == SuiteResult(
        id=1, run_id=1, suite_name="suite_name", suite_variables={"key": "value"}
    )


def test_map_to_dict():
    mapper = SuiteResultClassMapper()

    result = mapper.map_to_dict(
        SuiteResult(
            id=1, run_id=1, suite_name="suite_name", suite_variables={"key": "value"}
        )
    )

    assert result == {
        "id": 1,
        "run_id": 1,
        "suite_name": "suite_name",
        "suite_variables": {"key": "value"},
    }