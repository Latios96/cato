import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.branch_name import BranchName
from cato_common.domain.project import Project, ProjectStatus
from cato_common.domain.run import (
    Run,
)
from cato_common.domain.run_information import (
    OS,
    LocalComputerRunInformation,
    GithubActionsRunInformation,
)
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    _RunMapping,
    _LocalComputerRunInformationMapping,
)
from cato_common.utils.datetime_utils import aware_now_in_utc
from tests.unittests.cato_server.storage.conftest import sqltap_query_count_asserter


class TestConversionMethods:
    def test_to_entity(self, sqlalchemy_run_repository, local_computer_run_information):
        now = aware_now_in_utc()
        run = Run(
            id=1,
            project_id=2,
            run_batch_id=3,
            created_at=now,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )

        entity = sqlalchemy_run_repository.to_entity(run)

        assert entity.id == 1
        assert entity.project_entity_id == 2
        assert entity.run_batch_entity_id == 3
        assert entity.created_at == now

    def test_to_domain_object(
        self, sqlalchemy_run_repository, local_computer_run_information
    ):
        now = aware_now_in_utc()
        run_entity = _RunMapping(
            id=1,
            project_entity_id=2,
            run_batch_entity_id=3,
            created_at=now,
            branch_name="default",
            previous_run_id=None,
            run_information=_LocalComputerRunInformationMapping(
                id=0,
                run_entity_id=0,
                os="WINDOWS",
                computer_name="cray",
                local_username="username",
            ),
            performance_trace_entity_id=None,
        )

        run = sqlalchemy_run_repository.to_domain_object(run_entity)

        assert run == Run(
            id=1,
            project_id=2,
            run_batch_id=3,
            created_at=now,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )


class TestSave:
    def test_save_local_computer_run_information(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        local_computer_run_information,
    ):
        start_time = aware_now_in_utc()
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=start_time,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )

        run = sqlalchemy_run_repository.save(run)

        assert run == Run(
            id=1,
            project_id=1,
            run_batch_id=1,
            created_at=start_time,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=LocalComputerRunInformation(
                id=1,
                run_id=1,
                os=OS.WINDOWS,
                computer_name="cray",
                local_username="username",
            ),
            performance_trace_id=None,
        )

    def test_save_github_actions_run_information(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        github_actions_run_information,
    ):
        start_time = aware_now_in_utc()
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=start_time,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=github_actions_run_information,
            performance_trace_id=None,
        )

        run = sqlalchemy_run_repository.save(run)

        assert run == Run(
            id=1,
            project_id=1,
            run_batch_id=1,
            created_at=start_time,
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
            performance_trace_id=None,
        )

    def test_save_no_project_id(
        self, sqlalchemy_run_repository, run_batch, local_computer_run_information
    ):
        run = Run(
            id=0,
            project_id=2,
            run_batch_id=run_batch.id,
            created_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )

        with pytest.raises(IntegrityError):
            run = sqlalchemy_run_repository.save(run)

    def test_save_with_no_previous_run_id_is_possible(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        local_computer_run_information,
    ):
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )

        sqlalchemy_run_repository.save(run)

    def test_save_with_not_existing_previous_run_id_is_not_possible(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        local_computer_run_information,
    ):
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=42,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )

        with pytest.raises(IntegrityError):
            sqlalchemy_run_repository.save(run)


class TestFindById:
    def test_should_find(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        local_computer_run_information,
    ):
        start_time = aware_now_in_utc()
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=start_time,
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )
        run = sqlalchemy_run_repository.save(run)

        with sqltap_query_count_asserter(1):
            run = sqlalchemy_run_repository.find_by_id(run.id)

        assert run.project_id == project.id
        assert run.created_at == start_time

    def test_should_not_find(self, sqlalchemy_run_repository):
        assert not sqlalchemy_run_repository.find_by_id(100)


class FindByProjectId:
    def test_find_by_project_id_should_find_empty(self, sqlalchemy_run_repository):
        assert sqlalchemy_run_repository.find_by_project_id(10) == []

    def test_find_by_project_id_should_find_correct(
        self,
        sqlalchemy_run_repository,
        project,
        run_batch,
        local_computer_run_information,
    ):
        run = Run(
            id=0,
            project_id=project.id,
            run_batch_id=run_batch.id,
            created_at=aware_now_in_utc(),
            branch_name=BranchName("default"),
            previous_run_id=None,
            run_information=local_computer_run_information,
            performance_trace_id=None,
        )
        run = sqlalchemy_run_repository.save(run)

        with sqltap_query_count_asserter(1):
            runs_by_project_id = sqlalchemy_run_repository.find_by_project_id(
                project.id
            )

        assert runs_by_project_id == [run]


class TestFindByProjectIdPaginate:
    def test_should_find_empty(self, sqlalchemy_run_repository):
        page_request = PageRequest.first(10)

        assert sqlalchemy_run_repository.find_by_project_id_with_paging(
            10, page_request
        ) == Page.from_page_request(
            page_request=page_request, total_entity_count=0, entities=[]
        )

    def test_should_find_correct_single_run(
        self, sqlalchemy_run_repository, project, saving_run_factory
    ):
        run = saving_run_factory()

        page_request = PageRequest.first(10)

        with sqltap_query_count_asserter(2):
            runs = sqlalchemy_run_repository.find_by_project_id_with_paging(
                project.id, page_request
            )

        assert runs == Page.from_page_request(
            page_request=page_request, total_entity_count=1, entities=[run]
        )

    def test_should_find_correct_max_count_exceeding_page(
        self, sqlalchemy_run_repository, project, run_factory
    ):
        runs = sqlalchemy_run_repository.insert_many([run_factory() for x in range(21)])

        page_request = PageRequest.first(1)
        paging = sqlalchemy_run_repository.find_by_project_id_with_paging(
            project.id, page_request
        )
        assert paging == Page.from_page_request(
            page_request=page_request, total_entity_count=21, entities=[runs[20]]
        )

    def test_should_find_correct_max_count_exceeding_second_page(
        self, sqlalchemy_run_repository, project, run_factory
    ):
        runs = sqlalchemy_run_repository.insert_many([run_factory() for x in range(21)])

        page_request = PageRequest(page_size=5, page_number=2)

        assert sqlalchemy_run_repository.find_by_project_id_with_paging(
            project.id, page_request
        ) == Page.from_page_request(
            page_request=page_request,
            total_entity_count=21,
            entities=[runs[15], runs[14], runs[13], runs[12], runs[11]],
        )

    def test_should_filter_for_branches(
        self, sqlalchemy_run_repository, project, run_factory
    ):
        sqlalchemy_run_repository.save(
            run_factory(project_id=project.id, branch_name=BranchName("default"))
        )
        sqlalchemy_run_repository.save(
            run_factory(project_id=project.id, branch_name=BranchName("main"))
        )

        runs = sqlalchemy_run_repository.find_by_project_id_with_paging(
            project.id,
            PageRequest(page_size=5, page_number=1),
            RunFilterOptions(branches={BranchName("main")}),
        )

        assert len(runs.entities) == 1
        assert runs.entities[0].branch_name == BranchName("main")


class TestFindLastRunForProject:
    def test_should_return_none_for_empty_project(
        self, sqlalchemy_run_repository, project
    ):
        result = sqlalchemy_run_repository.find_last_run_for_project(
            project.id, BranchName("default")
        )

        assert result is None

    def test_should_return_first_run(
        self,
        sqlalchemy_project_repository,
        sqlalchemy_run_repository,
        project,
        run_factory,
    ):
        project2 = sqlalchemy_project_repository.save(
            Project(id=0, name="test", status=ProjectStatus.ACTIVE)
        )
        runs = sqlalchemy_run_repository.insert_many(
            [run_factory(project_id=project.id) for x in range(20)]
        )
        sqlalchemy_run_repository.insert_many(
            [run_factory(project_id=project2.id) for x in range(20)]
        )
        sqlalchemy_run_repository.insert_many(
            [run_factory(project_id=project.id, branch_name="dev") for x in range(20)]
        )

        result = sqlalchemy_run_repository.find_last_run_for_project(
            project.id, BranchName("default")
        )

        assert result == runs[19]


class TestFindBranchNamesForProject:
    def test_should_find_empty_list_for_not_existing_project(
        self, sqlalchemy_run_repository
    ):
        result = sqlalchemy_run_repository.find_branches_for_project(42)

        assert result == []

    def test_should_find_empty_list(self, sqlalchemy_run_repository, project):
        result = sqlalchemy_run_repository.find_branches_for_project(project.id)

        assert result == []

    def test_should_find_single_branch(self, sqlalchemy_run_repository, project, run):
        result = sqlalchemy_run_repository.find_branches_for_project(project.id)

        assert result == [BranchName("default")]

    def test_should_find_multiple_branches_and_sort(
        self, sqlalchemy_run_repository, project, run_factory
    ):
        sqlalchemy_run_repository.insert_many(
            [
                run_factory(project_id=project.id, branch_name=x)
                for x in [
                    BranchName("main"),
                    BranchName("dev"),
                    BranchName("legacy"),
                    BranchName("legacy"),
                    BranchName("legacy"),
                    BranchName("legacy"),
                    BranchName("legacy"),
                ]
            ]
        )

        result = sqlalchemy_run_repository.find_branches_for_project(project.id)

        assert result == [BranchName("dev"), BranchName("legacy"), BranchName("main")]


def test_delete_should_also_delete_run_information(
    sqlalchemy_run_repository,
    project,
    run_batch,
    local_computer_run_information,
    sessionmaker_fixture,
):
    start_time = aware_now_in_utc()
    run = Run(
        id=0,
        project_id=project.id,
        run_batch_id=run_batch.id,
        created_at=start_time,
        branch_name=BranchName("default"),
        previous_run_id=None,
        run_information=local_computer_run_information,
        performance_trace_id=None,
    )

    run = sqlalchemy_run_repository.save(run)
    assert run.id == 1

    sqlalchemy_run_repository.delete_by_id(run.id)

    assert sqlalchemy_run_repository.find_by_id(run.id) is None
    with sessionmaker_fixture() as session:
        run_information_result = (
            session.query(_LocalComputerRunInformationMapping)
            .filter(_LocalComputerRunInformationMapping.id == run.run_information.id)
            .first()
        )

    assert run_information_result is None
