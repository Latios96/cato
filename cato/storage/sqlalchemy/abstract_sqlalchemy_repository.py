from typing import TypeVar, Generic

T = TypeVar("T")
K = TypeVar("K")
E = TypeVar("K")


class AbstractSqlAlchemyRepository(Generic[T, E]):
    def __init__(self, session_maker):
        self._session_maker = session_maker

    def to_entity(self, domain_object: T) -> E:
        raise NotImplementedError()

    def to_domain_object(self, entity: E) -> T:
        raise NotImplementedError()
