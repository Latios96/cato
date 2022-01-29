import datetime
from typing import Optional

from sqlalchemy import Column, Integer, Text, DateTime

from cato_server.domain.auth.session import Session
from cato_server.domain.auth.session_id import SessionId
from cato_server.storage.abstract.session_repository import SessionRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
    T,
)


class _SessionMapping(Base):
    __tablename__ = "session_entity"
    id = Column(Text, nullable=False, primary_key=True)
    user_id = Column(Integer, nullable=False)
    created_at = Column(DateTime, nullable=False)
    expires_at = Column(DateTime, nullable=False)


class SqlAlchemySessionRepository(
    AbstractSqlAlchemyRepository[Session, _SessionMapping, SessionId], SessionRepository
):
    def to_entity(self, domain_object: Session) -> _SessionMapping:
        return _SessionMapping(
            id=str(domain_object.id) if domain_object.id != SessionId.none() else None,
            user_id=domain_object.user_id,
            created_at=domain_object.created_at,
            expires_at=domain_object.expires_at,
        )

    def to_domain_object(self, entity: _SessionMapping) -> Session:
        return Session(
            id=SessionId(entity.id),
            user_id=entity.user_id,
            created_at=entity.created_at,
            expires_at=entity.expires_at,
        )

    def mapping_cls(self):
        return _SessionMapping

    def save(self, domain_object: Session) -> T:
        session = self._session_maker()

        is_insert = domain_object.id == SessionId.none()

        session_mapping = self.to_entity(domain_object)

        if is_insert:
            session_mapping.id = str(SessionId.generate())
            session.add(session_mapping)
        else:
            session.merge(session_mapping)
        session.flush()

        domain_object = self.to_domain_object(session_mapping)

        session.commit()
        session.close()

        return domain_object

    def find_by_id(self, id: SessionId) -> Optional[T]:
        return super().find_by_id(str(id))

    def delete_by_id(self, id: SessionId) -> None:
        super().delete_by_id(str(id))

    def find_by_expires_at_is_older_than(self, date: datetime.datetime):
        session = self._session_maker()

        results = (
            session.query(_SessionMapping)
            .filter(_SessionMapping.expires_at < date)
            .all()
        )

        session.close()
        return self._map_many_to_domain_object(results)
