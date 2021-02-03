from typing import Iterable

from cato_server.domain.run import Run
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class RunRepository(AbstractRepository[Run, int]):
    def find_by_project_id(self, id: int) -> Iterable[Run]:
        raise NotImplementedError()
