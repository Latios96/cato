import datetime

from cato_server.domain.run import Run
from cato_server.mappers.run_class_mapper import RunClassMapper


def test_map_from_dict():
    started_at = datetime.datetime.now()
    mapper = RunClassMapper()

    result = mapper.map_from_dict(
        {"id": 1, "project_id": 1, "started_at": started_at.isoformat()}
    )

    assert result == Run(id=1, project_id=1, started_at=started_at)


def test_map_to_dict():
    started_at = datetime.datetime.now()
    mapper = RunClassMapper()

    result = mapper.map_to_dict(Run(id=1, project_id=1, started_at=started_at))

    assert result == {"id": 1, "project_id": 1, "started_at": started_at.isoformat()}
