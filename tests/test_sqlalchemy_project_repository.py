import pytest
from sqlalchemy.exc import IntegrityError

from cato.domain.project import Project
from cato.storage.sqlalchemy.sqlalchemy_project_repository import (
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

    project = repository.save(project)

    with pytest.raises(IntegrityError):
        project = repository.save(project)


def test_find_by_name_should_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")
    project = repository.save(project)

    assert repository.find_by_name("test_name").name == "test_name"


def test_find_by_name_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="dyfg")
    project = repository.save(project)

    assert not repository.find_by_name("test_name")


def test_find_by_id_should_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="test_name")
    project = repository.save(project)

    assert repository.find_by_id(project.id).name == "test_name"


def test_find_by_id_should_not_find(sessionmaker_fixture):
    repository = SqlAlchemyProjectRepository(sessionmaker_fixture)
    project = Project(id=0, name="dyfg")
    project = repository.save(project)

    assert not repository.find_by_id(100)


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
