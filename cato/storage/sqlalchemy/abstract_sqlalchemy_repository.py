from typing import TypeVar, Generic, Optional, Iterable

from sqlalchemy.ext.declarative import declarative_base

T = TypeVar("T")
K = TypeVar("K")
E = TypeVar("E")

Base = declarative_base()


class BaseEntity:
    id: int


class AbstractSqlAlchemyRepository(Generic[T, E, K]):
    def __init__(self, session_maker):
        self._session_maker = session_maker

    def save(self, domain_object: T) -> T:
        session = self._session_maker()

        is_insert = True if not domain_object.id else False

        project_mapping = self.to_entity(domain_object)

        if is_insert:
            session.add(project_mapping)
        else:
            session.merge(project_mapping)
        session.flush()

        domain_object = self.to_domain_object(project_mapping)

        session.commit()
        session.close()

        return domain_object

    def find_by_id(self, id: K) -> Optional[T]:
        session = self._session_maker()

        entity = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().id == id)
            .first()
        )
        if entity:
            return self.to_domain_object(entity)

    def find_all(self) -> Iterable[T]:
        session = self._session_maker()
        results = session.query(self.mapping_cls()).all()

        return [self.to_domain_object(x) for x in results]

    def to_entity(self, domain_object: T) -> E:
        raise NotImplementedError()

    def to_domain_object(self, entity: E) -> T:
        raise NotImplementedError()

    def mapping_cls(self):
        raise NotImplementedError()
