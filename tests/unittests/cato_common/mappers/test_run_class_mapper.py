import datetime

from cato_common.domain.run import Run


def test_map_from_dict(object_mapper):
    started_at = datetime.datetime.now()

    result = object_mapper.from_dict(
        {"id": 1, "project_id": 1, "started_at": started_at.isoformat()}, Run
    )

    assert result == Run(id=1, project_id=1, started_at=started_at)


def test_map_to_dict(object_mapper):
    started_at = datetime.datetime.now()

    result = object_mapper.to_dict(Run(id=1, project_id=1, started_at=started_at))

    assert result == {"id": 1, "project_id": 1, "started_at": started_at.isoformat()}
