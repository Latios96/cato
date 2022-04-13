import datetime

import pytest
from sqlalchemy.exc import IntegrityError

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.sqlalchemy.sqlalchemy_test_heartbeat_repository import (
    SqlAlchemyTestHeartbeatRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    SqlAlchemyTestResultRepository,
)
from cato_server.utils.datetime_utils import aware_now_in_utc


def test_should_save_test_heartbeat(sqlalchemy_test_heartbeat_repository, test_result):
    last_beat_datetime = aware_now_in_utc()
    test_heartbeat = TestHeartbeat(
        id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
    )

    test_heartbeat = sqlalchemy_test_heartbeat_repository.save(test_heartbeat)

    assert test_heartbeat == TestHeartbeat(
        id=1, test_result_id=test_result.id, last_beat=last_beat_datetime
    )


def test_should_not_save_test_heartbeat_duplicate_test_result_id(
    sqlalchemy_test_heartbeat_repository, test_result
):
    last_beat_datetime = aware_now_in_utc()
    sqlalchemy_test_heartbeat_repository.save(
        TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=last_beat_datetime)
    )

    with pytest.raises(IntegrityError):
        sqlalchemy_test_heartbeat_repository.save(
            TestHeartbeat(
                id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
            )
        )


def test_find_last_beat_older_than_should_return_correctly(
    sessionmaker_fixture,
    sqlalchemy_test_result_repository,
    sqlalchemy_test_heartbeat_repository,
    test_result,
):
    old_id = test_result.id
    test_result.id = 0
    test_result2 = sqlalchemy_test_result_repository.save(test_result)
    test_result.id = old_id
    now = aware_now_in_utc()
    two_weeks_ago = now - datetime.timedelta(weeks=2)
    sqlalchemy_test_heartbeat_repository.save(
        TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=now)
    )
    sqlalchemy_test_heartbeat_repository.save(
        TestHeartbeat(id=0, test_result_id=test_result2.id, last_beat=two_weeks_ago)
    )

    beats = sqlalchemy_test_heartbeat_repository.find_last_beat_older_than(
        now - datetime.timedelta(weeks=1)
    )

    assert beats == [TestHeartbeat(id=2, test_result_id=2, last_beat=two_weeks_ago)]


def test_find_last_beat_older_than_should_return_empty_no_heartbeats(
    sqlalchemy_test_heartbeat_repository,
):
    beats = sqlalchemy_test_heartbeat_repository.find_last_beat_older_than(
        aware_now_in_utc() - datetime.timedelta(weeks=1)
    )

    assert beats == []


def test_find_last_beat_older_than_should_return_empty(
    sqlalchemy_test_heartbeat_repository, test_result
):
    now = aware_now_in_utc()
    sqlalchemy_test_heartbeat_repository.save(
        TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=now)
    )

    beats = sqlalchemy_test_heartbeat_repository.find_last_beat_older_than(
        now - datetime.timedelta(weeks=1)
    )

    assert beats == []


def test_find_by_test_result_id_should_find(
    sqlalchemy_test_heartbeat_repository, test_result
):
    last_beat_datetime = aware_now_in_utc()
    test_heartbeat = TestHeartbeat(
        id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
    )
    sqlalchemy_test_heartbeat_repository.save(test_heartbeat)

    result = sqlalchemy_test_heartbeat_repository.find_by_test_result_id(test_result.id)

    assert result == TestHeartbeat(
        id=1, test_result_id=test_result.id, last_beat=last_beat_datetime
    )


def test_find_by_test_result_id_should_not_find(
    sqlalchemy_test_heartbeat_repository, test_result
):
    last_beat_datetime = aware_now_in_utc()
    test_heartbeat = TestHeartbeat(
        id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
    )
    sqlalchemy_test_heartbeat_repository.save(test_heartbeat)

    result = sqlalchemy_test_heartbeat_repository.find_by_test_result_id(42)

    assert result is None


def test_delete_by_id_should_delete(sqlalchemy_test_heartbeat_repository, test_result):
    last_beat_datetime = aware_now_in_utc()
    test_heartbeat = sqlalchemy_test_heartbeat_repository.save(
        TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=last_beat_datetime)
    )

    sqlalchemy_test_heartbeat_repository.delete_by_id(test_heartbeat.id)

    assert not sqlalchemy_test_heartbeat_repository.find_by_id(test_heartbeat.id)


def test_delete_by_id_should_raise_not_existing(sqlalchemy_test_heartbeat_repository):
    with pytest.raises(ValueError):
        sqlalchemy_test_heartbeat_repository.delete_by_id(42)
