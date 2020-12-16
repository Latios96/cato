from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    ExecutionStatus,
)
from cato_server.mappers.create_full_run_dto_class_mapper import (
    CreateFullRunDtoClassMapper,
)


def test_map_from():
    source_dict = {
        "project_id": 1,
        "test_suites": [
            {
                "suite_name": "my_suite",
                "suite_variables": {},
                "tests": [
                    {
                        "execution_status": "NOT_STARTED",
                        "test_command": "cmd",
                        "test_identifier": "test/identifier",
                        "test_name": "test_name",
                        "test_variables": {},
                    }
                ],
            }
        ],
    }
    mapper = CreateFullRunDtoClassMapper()

    result = mapper.map_from_dict(source_dict)

    assert result == CreateFullRunDto(
        project_id=1,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        ExecutionStatus.NOT_STARTED,
                        "cmd",
                        "test/identifier",
                        "test_name",
                        {},
                    )
                ],
            )
        ],
    )


def test_map_to():
    dto = CreateFullRunDto(
        project_id=1,
        test_suites=[
            TestSuiteForRunCreation(
                suite_name="my_suite",
                suite_variables={},
                tests=[
                    TestForRunCreation(
                        ExecutionStatus.NOT_STARTED,
                        "cmd",
                        "test/identifier",
                        "test_name",
                        {},
                    )
                ],
            )
        ],
    )
    mapper = CreateFullRunDtoClassMapper()

    result = mapper.map_to_dict(dto)

    assert result == {
        "project_id": 1,
        "test_suites": [
            {
                "suite_name": "my_suite",
                "suite_variables": {},
                "tests": [
                    {
                        "execution_status": "NOT_STARTED",
                        "test_command": "cmd",
                        "test_identifier": "test/identifier",
                        "test_name": "test_name",
                        "test_variables": {},
                    }
                ],
            }
        ],
    }
