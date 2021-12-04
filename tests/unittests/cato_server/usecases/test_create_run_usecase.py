import datetime

from freezegun import freeze_time

from cato_api_models.catoapimodels import (
    CreateFullRunDto,
    TestSuiteForRunCreation,
    TestForRunCreation,
    ComparisonSettingsDto,
    ComparisonMethodDto,
)
from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
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

STARTED_AT = datetime.datetime(2021, 12, 4, 15, 8)

TEST_SUITES = [
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
]


@freeze_time(STARTED_AT)
def test_should_create_without_branch_name_and_no_previous_run(
    sessionmaker_fixture, project, object_mapper
):
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
            test_suites=TEST_SUITES,
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    assert test_result_repository.find_by_id(1).machine_info == None
    assert test_result_repository.find_by_id(1).failure_reason == None


@freeze_time(STARTED_AT)
def test_should_create_with_explicit_branch_name_and_no_previous_run(
    sessionmaker_fixture, project, object_mapper
):
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
            test_suites=TEST_SUITES,
            branch_name="main",
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        started_at=STARTED_AT,
        branch_name=BranchName("main"),
        previous_run_id=None,
    )
    assert test_result_repository.find_by_id(1).machine_info == None
    assert test_result_repository.find_by_id(1).failure_reason == None


@freeze_time(STARTED_AT)
def test_should_create_with_previous_run(
    sessionmaker_fixture, project, object_mapper, run_factory
):
    run_repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    previous_run = run_repository.save(run_factory(project_id=project.id))
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
            test_suites=TEST_SUITES,
        )
    )

    assert run == Run(
        id=2,
        project_id=project.id,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=previous_run.id,
    )
    assert test_result_repository.find_by_id(1).machine_info == None
    assert test_result_repository.find_by_id(1).failure_reason == None
