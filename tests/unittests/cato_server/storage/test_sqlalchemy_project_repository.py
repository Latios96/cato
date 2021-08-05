import pytest
from sqlalchemy.exc import IntegrityError

from cato_common.domain.project import Project
from cato_server.storage.sqlalchemy.sqlalchemy_project_repository import (
    SqlAlchemyProjectRepository,
    _ProjectMapping,
)


def test_save(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")

    project = repository.save(project)

    assert project.id == 1
    assert project.name == "test_name"


def test_save_name_should_be_unique(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")

    repository.save(project)

    with pytest.raises(IntegrityError):
        repository.save(Project(id=0, name="test_name"))


def test_insert_many_should_insert(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project1 = Project(id=0, name="test_name1")
    project2 = Project(id=0, name="test_name2")
    project3 = Project(id=0, name="test_name3")

    projects = repository.insert_many([project1, project2, project3])

    assert projects == [
        Project(id=1, name="test_name1"),
        Project(id=2, name="test_name2"),
        Project(id=3, name="test_name3"),
    ]


def test_find_by_name_should_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")
    repository.save(project)

    assert repository.find_by_name("test_name").name == "test_name"


def test_find_by_name_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="dyfg")
    repository.save(project)

    assert not repository.find_by_name("test_name")


def test_find_by_id_should_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")
    project = repository.save(project)

    assert repository.find_by_id(project.id).name == "test_name"


def test_find_by_id_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="dyfg")
    repository.save(project)

    by_id = repository.find_by_id(100)
    assert not by_id


def test_to_entity(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)

    project = Project(id=1, name="test")

    entity = repository.to_entity(project)

    assert entity.id == 1
    assert entity.name == "test"


def test_to_domain_object(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)

    entity = _ProjectMapping(id=1, name="test")

    domain_object = repository.to_domain_object(entity)

    assert domain_object.id == 1
    assert domain_object.name == "test"
