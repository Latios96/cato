import datetime
from typing import Iterable, Optional

from sqlalchemy import Column, Integer, ForeignKey, DateTime

from cato_server.domain.test_heartbeat import TestHeartbeat
from cato_server.storage.abstract.test_heartbeat_repository import (
    TestHeartbeatRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class TestHeartbeatMapping(Base):
    __tablename__ = "test_heartbeat_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_result_entity_id = Column(
        Integer, ForeignKey("test_result_entity.id"), unique=True
    )
    last_beat = Column(DateTime, nullable=False)


class SqlAlchemyTestHeartbeatRepository(
    AbstractSqlAlchemyRepository[TestHeartbeat, TestHeartbeatMapping, int],
    TestHeartbeatRepository,
):
    def to_entity(self, domain_object: TestHeartbeat) -> TestHeartbeatMapping:
        return TestHeartbeatMapping(
            id=domain_object.id if domain_object.id else None,
            test_result_entity_id=domain_object.test_result_id,
            last_beat=domain_object.last_beat,
        )

    def to_domain_object(self, entity: TestHeartbeatMapping) -> TestHeartbeat:
        return TestHeartbeat(
            id=entity.id,
            test_result_id=entity.test_result_entity_id,
            last_beat=entity.last_beat,
        )

    def mapping_cls(self):
        return TestHeartbeatMapping

    def find_by_test_result_id(self, test_result_id) -> Optional[TestHeartbeat]:
        session = self._session_maker()

        query = session.query(self.mapping_cls()).filter(
            self.mapping_cls().test_result_entity_id == test_result_id
        )
        session.close()
        return self._map_one_to_domain_object(query.first())

    def find_last_beat_older_than(
        self, date: datetime.datetime
    ) -> Iterable[TestHeartbeat]:
        session = self._session_maker()

        results = (
            session.query(TestHeartbeatMapping)
            .filter(TestHeartbeatMapping.last_beat < date)
            .all()
        )

        session.close()
        return self._map_many_to_domain_object(results)
