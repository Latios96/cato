import datetime

from freezegun import freeze_time

from cato.domain.comparison_settings import ComparisonSettings
from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.dtos.create_full_run_dto import (
    TestSuiteForRunCreation,
    TestForRunCreation,
    CreateFullRunDto,
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
from cato_server.usecases.create_run import CreateRunUsecase

STARTED_AT = datetime.datetime(2021, 12, 4, 15, 8)

TEST_SUITES = [
    TestSuiteForRunCreation(
        suite_name="my_suite",
        suite_variables={},
        tests=[
            TestForRunCreation(
                test_command="cmd",
                test_identifier=TestIdentifier.from_string("test/identifier"),
                test_name="test_name",
                test_variables={},
                comparison_settings=ComparisonSettings.default(),
            )
        ],
    )
]


@freeze_time(STARTED_AT)
def test_should_create_without_branch_name_and_no_previous_run(
    sqlalchemy_run_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
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
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None


@freeze_time(STARTED_AT)
def test_should_create_with_explicit_branch_name_and_no_previous_run(
    sqlalchemy_run_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            test_suites=TEST_SUITES,
            branch_name=BranchName("main"),
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        started_at=STARTED_AT,
        branch_name=BranchName("main"),
        previous_run_id=None,
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None


@freeze_time(STARTED_AT)
def test_should_create_with_previous_run(
    sessionmaker_fixture,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
    run_factory,
    sqlalchemy_suite_result_repository,
    sqlalchemy_run_repository,
):
    previous_run = sqlalchemy_run_repository.save(run_factory(project_id=project.id))
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
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
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None
