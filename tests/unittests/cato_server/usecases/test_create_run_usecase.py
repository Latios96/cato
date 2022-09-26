import datetime

from dateutil.tz import tzlocal
from freezegun import freeze_time

from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import Run
from cato_common.domain.run_information import (
    OS,
    LocalComputerRunInformation,
    GithubActionsRunInformation,
)
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.dtos.create_full_run_dto import (
    TestSuiteForRunCreation,
    TestForRunCreation,
    CreateFullRunDto,
    LocalComputerRunInformationForRunCreation,
    GithubActionsRunInformationForRunCreation,
)
from cato_server.usecases.create_run import CreateRunUsecase

STARTED_AT = datetime.datetime(2021, 12, 4, 15, 8, tzinfo=tzlocal())

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
    sqlalchemy_run_batch_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
    run_batch_identifier,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_run_batch_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            run_information=LocalComputerRunInformationForRunCreation(
                os=OS.WINDOWS, computer_name="cray", local_username="username"
            ),
            test_suites=TEST_SUITES,
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        run_batch_id=1,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=None,
        run_information=LocalComputerRunInformation(
            id=1,
            run_id=1,
            os=OS.WINDOWS,
            computer_name="cray",
            local_username="username",
        ),
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None
    assert sqlalchemy_run_batch_repository.find_by_id(1).runs == [run]
    assert (
        sqlalchemy_run_batch_repository.find_by_id(1).run_batch_identifier
        == run_batch_identifier
    )


@freeze_time(STARTED_AT)
def test_should_create_with_local_run_information(
    sqlalchemy_run_repository,
    sqlalchemy_run_batch_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
    run_batch_identifier,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_run_batch_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            run_information=LocalComputerRunInformationForRunCreation(
                os=OS.WINDOWS, computer_name="cray", local_username="username"
            ),
            test_suites=TEST_SUITES,
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        run_batch_id=1,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=None,
        run_information=LocalComputerRunInformation(
            id=1,
            run_id=1,
            os=OS.WINDOWS,
            computer_name="cray",
            local_username="username",
        ),
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None
    assert sqlalchemy_run_batch_repository.find_by_id(1).runs == [run]
    assert (
        sqlalchemy_run_batch_repository.find_by_id(1).run_batch_identifier
        == run_batch_identifier
    )


@freeze_time(STARTED_AT)
def test_should_create_with_github_actions_run_information(
    sqlalchemy_run_repository,
    sqlalchemy_run_batch_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
    run_batch_identifier,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_run_batch_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            run_information=GithubActionsRunInformationForRunCreation(
                os=OS.LINUX,
                computer_name="cray",
                github_run_id=3052454707,
                html_url="https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
                job_name="build_ubuntu",
                actor="Latios96",
                attempt=1,
                run_number=2,
                github_url="https://github.com",
                github_api_url="https://api.github.com",
            ),
            test_suites=TEST_SUITES,
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        run_batch_id=1,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=None,
        run_information=GithubActionsRunInformation(
            id=1,
            run_id=1,
            os=OS.LINUX,
            computer_name="cray",
            github_run_id=3052454707,
            html_url="https://github.com/owner/repo-name/actions/runs/3052454707/jobs/4921861789",
            job_name="build_ubuntu",
            actor="Latios96",
            attempt=1,
            run_number=2,
            github_url="https://github.com",
            github_api_url="https://api.github.com",
        ),
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None
    assert sqlalchemy_run_batch_repository.find_by_id(1).runs == [run]
    assert (
        sqlalchemy_run_batch_repository.find_by_id(1).run_batch_identifier
        == run_batch_identifier
    )


@freeze_time(STARTED_AT)
def test_should_create_with_explicit_branch_name_and_no_previous_run(
    sqlalchemy_run_repository,
    sqlalchemy_run_batch_repository,
    sqlalchemy_suite_result_repository,
    sqlalchemy_test_result_repository,
    project,
    object_mapper,
    run_batch_identifier,
):
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_run_batch_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            test_suites=TEST_SUITES,
            run_information=LocalComputerRunInformationForRunCreation(
                os=OS.WINDOWS, computer_name="cray", local_username="username"
            ),
            branch_name=BranchName("main"),
        )
    )

    assert run == Run(
        id=1,
        project_id=project.id,
        run_batch_id=1,
        started_at=STARTED_AT,
        branch_name=BranchName("main"),
        previous_run_id=None,
        run_information=LocalComputerRunInformation(
            id=1,
            run_id=1,
            os=OS.WINDOWS,
            computer_name="cray",
            local_username="username",
        ),
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None


@freeze_time(STARTED_AT)
def test_should_create_with_previous_run(
    sessionmaker_fixture,
    sqlalchemy_test_result_repository,
    sqlalchemy_run_batch_repository,
    project,
    object_mapper,
    run_factory,
    sqlalchemy_suite_result_repository,
    sqlalchemy_run_repository,
    saving_run_batch_factory,
    run_batch_identifier,
):
    previous_run = sqlalchemy_run_repository.save(
        run_factory(project_id=project.id, run_batch_id=saving_run_batch_factory().id)
    )
    usecase = CreateRunUsecase(
        sqlalchemy_run_repository,
        sqlalchemy_run_batch_repository,
        sqlalchemy_suite_result_repository,
        sqlalchemy_test_result_repository,
        object_mapper,
    )

    run = usecase.create_run(
        CreateFullRunDto(
            project_id=project.id,
            run_batch_identifier=run_batch_identifier,
            test_suites=TEST_SUITES,
            run_information=LocalComputerRunInformationForRunCreation(
                os=OS.WINDOWS, computer_name="cray", local_username="username"
            ),
        )
    )

    assert run == Run(
        id=2,
        project_id=project.id,
        run_batch_id=2,
        started_at=STARTED_AT,
        branch_name=BranchName("default"),
        previous_run_id=previous_run.id,
        run_information=LocalComputerRunInformation(
            id=2,
            run_id=2,
            os=OS.WINDOWS,
            computer_name="cray",
            local_username="username",
        ),
    )
    assert sqlalchemy_test_result_repository.find_by_id(1).machine_info == None
    assert sqlalchemy_test_result_repository.find_by_id(1).failure_reason == None
