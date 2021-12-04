import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.branch_name import BranchName
from cato_common.domain.project import Project
from cato_common.domain.run import Run
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import (
    SqlAlchemyRunRepository,
    _RunMapping,
)


def test_to_entity(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    run = Run(
        id=1,
        project_id=2,
        started_at=now,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )

    entity = repository.to_entity(run)

    assert entity.id == 1
    assert entity.project_entity_id == 2
    assert entity.started_at == now


def test_to_domain_object(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    run_entity = _RunMapping(
        id=1,
        project_entity_id=2,
        started_at=now,
        branch_name="default",
        previous_run_id=None,
    )

    run = repository.to_domain_object(run_entity)

    assert run == Run(
        id=1,
        project_id=2,
        started_at=now,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )


def test_save(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    run = Run(
        id=0,
        project_id=project.id,
        started_at=start_time,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )

    run = repository.save(run)

    assert run.id == 1
    assert run.project_id == 1
    assert run.started_at == start_time


def test_save_no_project_id(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(
        id=0,
        project_id=2,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )

    with pytest.raises(IntegrityError):
        run = repository.save(run)


def test_save_with_no_previous_run_id_is_possible(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )

    repository.save(run)


def test_save_with_not_existing_previous_run_id_is_not_possible(
    sessionmaker_fixture, project
):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=42,
    )

    with pytest.raises(IntegrityError):
        repository.save(run)


def test_find_by_id_should_find(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    start_time = datetime.datetime.now()
    run = Run(
        id=0,
        project_id=project.id,
        started_at=start_time,
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    run = repository.save(run)

    assert repository.find_by_id(run.id).project_id == project.id
    assert repository.find_by_id(run.id).started_at == start_time


def test_find_by_id_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)

    assert not repository.find_by_id(100)


def test_find_by_project_id_should_find_empty(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)

    assert repository.find_by_project_id(10) == []


def test_find_by_project_id_should_find_correct(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)

    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    run = repository.save(run)

    assert repository.find_by_project_id(project.id) == [run]


def test_find_by_project_id_paginate_should_find_empty(sessionmaker_fixture):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)

    page_request = PageRequest.first(10)

    assert repository.find_by_project_id_with_paging(
        10, page_request
    ) == Page.from_page_request(
        page_request=page_request, total_entity_count=0, entities=[]
    )


def test_find_by_project_id_paginate_should_find_correct(sessionmaker_fixture, project):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)

    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    run = repository.save(run)

    page_request = PageRequest.first(10)

    assert repository.find_by_project_id_with_paging(
        project.id, page_request
    ) == Page.from_page_request(
        page_request=page_request, total_entity_count=1, entities=[run]
    )


def test_find_by_project_id_paginate_should_find_correct_max_count_exceeding_page(
    sessionmaker_fixture, project
):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    repository.save(run)
    runs = repository.insert_many(
        [
            Run(
                id=0,
                project_id=project.id,
                started_at=datetime.datetime.now(),
                branch_name=BranchName("default"),
                previous_run_id=None,
            )
            for x in range(20)
        ]
    )

    page_request = PageRequest.first(1)

    assert repository.find_by_project_id_with_paging(
        project.id, page_request
    ) == Page.from_page_request(
        page_request=page_request, total_entity_count=21, entities=[runs[19]]
    )


def test_find_by_project_id_paginate_should_find_correct_max_count_exceeding_second_page(
    sessionmaker_fixture, project
):
    repository = SqlAlchemyRunRepository(sessionmaker_fixture)
    run = Run(
        id=0,
        project_id=project.id,
        started_at=datetime.datetime.now(),
        branch_name=BranchName("default"),
        previous_run_id=None,
    )
    run = repository.save(run)
    runs = repository.insert_many(
        [
            Run(
                id=0,
                project_id=project.id,
                started_at=datetime.datetime.now(),
                branch_name=BranchName("default"),
                previous_run_id=None,
            )
            for x in range(20)
        ]
    )

    page_request = PageRequest(page_size=5, page_number=2)

    assert repository.find_by_project_id_with_paging(
        project.id, page_request
    ) == Page.from_page_request(
        page_request=page_request,
        total_entity_count=21,
        entities=[runs[14], runs[13], runs[12], runs[11], runs[10]],
    )


class TestFindLastRunForProject:
    def test_should_return_none_for_empty_project(self, sessionmaker_fixture, project):
        repository = SqlAlchemyRunRepository(sessionmaker_fixture)

        result = repository.find_last_run_for_project(project.id, BranchName("default"))

        assert result is None

    def test_should_return_first_run(self, sessionmaker_fixture, project, run_factory):
        project2 = SqlAlchemyProjectRepository(sessionmaker_fixture).save(
            Project(id=0, name="test")
        )
        repository = SqlAlchemyRunRepository(sessionmaker_fixture)
        runs = repository.insert_many(
            [run_factory(project_id=project.id) for x in range(20)]
        )
        repository.insert_many([run_factory(project_id=project2.id) for x in range(20)])
        repository.insert_many(
            [run_factory(project_id=project.id, branch_name="dev") for x in range(20)]
        )

        result = repository.find_last_run_for_project(project.id, BranchName("default"))

        assert result == runs[19]
