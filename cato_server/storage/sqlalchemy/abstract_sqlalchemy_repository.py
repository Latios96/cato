from typing import TypeVar, Generic, Optional, Iterable, Callable

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

from cato_server.storage.abstract.page import PageRequest, Page

T = TypeVar("T")
K = TypeVar("K")
E = TypeVar("E")

Base = declarative_base()


class BaseEntity:
    id: int


class AbstractSqlAlchemyRepository(Generic[T, E, K]):
    _session_maker: Callable[[], Session]

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

    def insert_many(self, domain_objects: Iterable[T]) -> Iterable[T]:
        session = self._session_maker()

        project_mappings = list(map(self.to_entity, domain_objects))

        session.bulk_save_objects(project_mappings, return_defaults=True)

        session.flush()
        session.commit()
        session.close()

        domain_objects = list(map(self.to_domain_object, project_mappings))

        return domain_objects

    def find_by_id(self, id: K) -> Optional[T]:
        session = self._session_maker()

        query = session.query(self.mapping_cls()).filter(self.mapping_cls().id == id)
        session.close()
        return self._map_one_to_domain_object(query.first())

    def find_all(self) -> Iterable[T]:
        session = self._session_maker()
        results = session.query(self.mapping_cls()).all()

        session.close()
        return self._map_many_to_domain_object(results)

    def find_all_with_paging(self, page_request: PageRequest) -> Page[T]:
        session = self._session_maker()

        page = self._pageginate(
            session, session.query(self.mapping_cls()), page_request
        )

        session.close()
        return page

    def delete_by_id(self, id: K):
        session = self._session_maker()
        entity = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().id == id)
            .first()
        )
        if not entity:
            session.close()
            raise ValueError(f"No entity with id {id} exists!")
        session.delete(entity)
        session.commit()
        session.close()

    def to_entity(self, domain_object: T) -> E:
        raise NotImplementedError()

    def to_domain_object(self, entity: E) -> T:
        raise NotImplementedError()

    def mapping_cls(self):
        raise NotImplementedError()

    def _map_one_to_domain_object(self, entity):
        if entity:
            return self.to_domain_object(entity)

    def _map_many_to_domain_object(self, entities):
        return [self.to_domain_object(x) for x in entities]

    def _pageginate(self, session, query, page_request) -> Page[T]:
        results = query.limit(page_request.page_size).offset(page_request.offset).all()
        total_count = query.count()
        page = Page.from_page_request(
            page_request, total_count, self._map_many_to_domain_object(results)
        )
        return page
