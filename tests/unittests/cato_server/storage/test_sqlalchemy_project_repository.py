import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.project import Project, ProjectStatus
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
    _ProjectMapping,
)


def test_save(sqlalchemy_project_repository):
    project = Project(id=0, name="test_name", status=ProjectStatus.ACTIVE)

    project = sqlalchemy_project_repository.save(project)

    assert project.id == 1
    assert project.name == "test_name"


def test_save_name_should_be_unique(sqlalchemy_project_repository):
    project = Project(id=0, name="test_name", status=ProjectStatus.ACTIVE)

    sqlalchemy_project_repository.save(project)

    with pytest.raises(IntegrityError):
        sqlalchemy_project_repository.save(
            Project(id=0, name="test_name", status=ProjectStatus.ACTIVE)
        )


def test_insert_many_should_insert(sqlalchemy_project_repository):
    project1 = Project(id=0, name="test_name1", status=ProjectStatus.ACTIVE)
    project2 = Project(id=0, name="test_name2", status=ProjectStatus.ACTIVE)
    project3 = Project(id=0, name="test_name3", status=ProjectStatus.ACTIVE)

    projects = sqlalchemy_project_repository.insert_many([project1, project2, project3])

    assert projects == [
        Project(id=1, name="test_name1", status=ProjectStatus.ACTIVE),
        Project(id=2, name="test_name2", status=ProjectStatus.ACTIVE),
        Project(id=3, name="test_name3", status=ProjectStatus.ACTIVE),
    ]


def test_find_by_name_should_find(sqlalchemy_project_repository):
    project = Project(id=0, name="test_name", status=ProjectStatus.ACTIVE)
    sqlalchemy_project_repository.save(project)

    assert sqlalchemy_project_repository.find_by_name("test_name").name == "test_name"


def test_find_by_name_should_not_find(sqlalchemy_project_repository):
    project = Project(id=0, name="dyfg", status=ProjectStatus.ACTIVE)
    sqlalchemy_project_repository.save(project)

    assert not sqlalchemy_project_repository.find_by_name("test_name")


def test_find_by_id_should_find(sqlalchemy_project_repository):
    project = Project(id=0, name="test_name", status=ProjectStatus.ACTIVE)
    project = sqlalchemy_project_repository.save(project)

    assert sqlalchemy_project_repository.find_by_id(project.id).name == "test_name"


def test_find_by_id_should_not_find(sqlalchemy_project_repository):
    project = Project(id=0, name="dyfg", status=ProjectStatus.ACTIVE)
    sqlalchemy_project_repository.save(project)

    by_id = sqlalchemy_project_repository.find_by_id(100)
    assert not by_id


def test_to_entity(sqlalchemy_project_repository):
    project = Project(id=1, name="test", status=ProjectStatus.ACTIVE)

    entity = sqlalchemy_project_repository.to_entity(project)

    assert entity.id == 1
    assert entity.name == "test"
    assert entity.status == "ACTIVE"


def test_to_domain_object(sqlalchemy_project_repository):
    entity = _ProjectMapping(id=1, name="test", status="ACTIVE")

    domain_object = sqlalchemy_project_repository.to_domain_object(entity)

    assert domain_object.id == 1
    assert domain_object.name == "test"
    assert domain_object.status == "ACTIVE"
