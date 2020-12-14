from cato.domain.project import Project
from cato.mappers.project_class_mapper import ProjectClassMapper


def test_map_from_dict():
    mapper = ProjectClassMapper()

    result = mapper.map_from_dict({"id": 1, "name": "project"})

    assert result == Project(id=1, name="project")


def test_map_to_dict():
    mapper = ProjectClassMapper()

    result = mapper.map_to_dict(Project(id=1, name="project"))

    assert result == {"id": 1, "name": "project"}
