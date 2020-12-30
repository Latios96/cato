from cato_server.domain.project import Project
from cato_server.mappers.internal.mapper_registry import MapperRegistry
from cato_server.mappers.internal.project_class_mapper import ProjectClassMapper


def test_register_and_get():
    mapper_registry = MapperRegistry()
    mapper = ProjectClassMapper()

    mapper_registry.register_mapper(Project, mapper)
    returned_mapper = mapper_registry.class_mapper_for_cls(Project)

    assert returned_mapper is mapper


def test_no_mapper_exists():
    mapper_registry = MapperRegistry()

    assert not mapper_registry.class_mapper_for_cls(Project)
