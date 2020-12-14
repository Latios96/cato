from typing import Optional, Iterable

from cato_server.domain.run import Run
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class RunRepository(AbstractRepository[Run, int]):
    def save(self, run: Run) -> Run:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[Run]:
        raise NotImplementedError()

    def find_by_project_id(self, id: int) -> Iterable[Run]:
        raise NotImplementedError()
