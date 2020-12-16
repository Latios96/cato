from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    ExecutionStatus,
    MachineInfo,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    SqlAlchemySuiteResultRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.usecases.create_full_run import CreateFullRunUsecase


def test_should_create(sessionmaker_fixture, project):
    run_repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    suite_result_repository = SqlAlchemySuiteResultRepository(sessionmaker_fixture)
    test_result_repository = SqlAlchemyTestResultRepository(sessionmaker_fixture)
    usecase = CreateFullRunUsecase(
        run_repository, suite_result_repository, test_result_repository
    )

    run = usecase.create_full_run(
        CreateFullRunDto(
            project_id=project.id,
            test_suites=[
                TestSuiteForRunCreation(
                    suite_name="my_suite",
                    suite_variables={},
                    tests=[
                        TestForRunCreation(
                            ExecutionStatus.NOT_STARTED,
                            MachineInfo(cpu_name="test", cores=8, memory=8),
                            "cmd",
                            "test/identifier",
                            "test_name",
                            {},
                        )
                    ],
                )
            ],
        )
    )

    assert run.id == 1
    assert run.started_at
