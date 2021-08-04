from cato_server.domain.project import Project


def test_map_from_dict(object_mapper):
    result = object_mapper.from_dict({"id": 1, "name": "project"}, Project)

    assert result == Project(id=1, name="project")


def test_map_to_dict(object_mapper):
    result = object_mapper.to_dict(Project(id=1, name="project"))

    assert result == {"id": 1, "name": "project"}
