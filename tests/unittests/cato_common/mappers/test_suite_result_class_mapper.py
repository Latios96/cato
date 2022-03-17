from cato_common.domain.suite_result import SuiteResult


def test_map_from_dict(object_mapper):
    result = object_mapper.from_dict(
        {
            "id": 1,
            "runId": 1,
            "suiteName": "suite_name",
            "suiteVariables": {"key": "value"},
        },
        SuiteResult,
    )

    assert result == SuiteResult(
        id=1, run_id=1, suite_name="suite_name", suite_variables={"key": "value"}
    )


def test_map_to_dict(object_mapper):
    result = object_mapper.to_dict(
        SuiteResult(
            id=1, run_id=1, suite_name="suite_name", suite_variables={"key": "value"}
        )
    )

    assert result == {
        "id": 1,
        "runId": 1,
        "suiteName": "suite_name",
        "suiteVariables": {"key": "value"},
    }
