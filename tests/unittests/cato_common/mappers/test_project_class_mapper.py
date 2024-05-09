from cato_common.domain.project import Project, ProjectStatus


def test_map_from_dict(object_mapper):
    result = object_mapper.from_dict(
        {"id": 1, "name": "project", "status": "ACTIVE"}, Project
    )

    assert result == Project(id=1, name="project", status=ProjectStatus.ACTIVE)


def test_map_to_dict(object_mapper):
    result = object_mapper.to_dict(
        Project(id=1, name="project", status=ProjectStatus.ACTIVE)
    )

    assert result == {"id": 1, "name": "project", "status": "ACTIVE"}
