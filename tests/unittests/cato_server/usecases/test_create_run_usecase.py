from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    ComparisonSettingsDto,
    ComparisonMethodDto,
)
from cato_api_models.catoapimodels import RunDto, RunStatusDto
from cato_server.domain.event import Event
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.usecases.create_run import CreateRunUsecase


def test_should_create(sessionmaker_fixture, project, object_mapper):
    run_repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    suite_result_repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    test_result_repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    usecase = CreateRunUsecase(
        run_repository,
        suite_result_repository,
        test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            test_suites=[
                TestSuiteForRunCreation(
                    suite_name="my_suite",
                    suite_variables={},
                    tests=[
                        TestForRunCreation(
                            test_command="cmd",
                            test_identifier="test/identifier",
                            test_name="test_name",
                            test_variables={},
                            comparison_settings=ComparisonSettingsDto(
                                method=ComparisonMethodDto.SSIM, threshold=0.8
                            ),
                        )
                    ],
                )
            ],
        )
    )

    assert run.id == 1
    assert run.started_at
    assert test_result_repository.find_by_id(1).machine_info == None
