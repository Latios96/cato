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


def test_should_save_test_heartbeat(sessionmaker_fixture, test_result):
    repository = SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)
    last_beat_datetime = datetime.datetime.now()
    test_heartbeat = TestHeartbeat(
        id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
    )

    test_heartbeat = repository.save(test_heartbeat)

    assert test_heartbeat == TestHeartbeat(
        id=1, test_result_id=test_result.id, last_beat=last_beat_datetime
    )


def test_should_not_save_test_heartbeat_duplicate_test_result_id(
    sessionmaker_fixture, test_result
):
    repository = SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)
    last_beat_datetime = datetime.datetime.now()
    repository.save(
        TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=last_beat_datetime)
    )

    with pytest.raises(IntegrityError):
        repository.save(
            TestHeartbeat(
                id=0, test_result_id=test_result.id, last_beat=last_beat_datetime
            )
        )


def test_find_last_beat_older_than_should_return_correctly(
    sessionmaker_fixture, test_result
):
    old_id = test_result.id
    test_result.id = 0
    test_result2 = SqlAlchemyTestResultRepository(sessionmaker_fixture).save(
        test_result
    )
    test_result.id = old_id
    repository = SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    two_weeks_ago = now - datetime.timedelta(weeks=2)
    repository.save(TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=now))
    repository.save(
        TestHeartbeat(id=0, test_result_id=test_result2.id, last_beat=two_weeks_ago)
    )

    beats = repository.find_last_beat_older_than(now - datetime.timedelta(weeks=1))

    assert beats == [TestHeartbeat(id=2, test_result_id=2, last_beat=two_weeks_ago)]


def test_find_last_beat_older_than_should_return_empty_no_heartbeats(
    sessionmaker_fixture,
):
    repository = SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)

    beats = repository.find_last_beat_older_than(
        datetime.datetime.now() - datetime.timedelta(weeks=1)
    )

    assert beats == []


def test_find_last_beat_older_than_should_return_empty(
    sessionmaker_fixture, test_result
):
    repository = SqlAlchemyTestHeartbeatRepository(sessionmaker_fixture)
    now = datetime.datetime.now()
    repository.save(TestHeartbeat(id=0, test_result_id=test_result.id, last_beat=now))

    beats = repository.find_last_beat_older_than(now - datetime.timedelta(weeks=1))

    assert beats == []
