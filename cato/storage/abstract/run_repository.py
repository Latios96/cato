from typing import Optional

from cato.domain.run import Run
from cato.storage.abstract.abstract_repository import AbstractRepository, K, T


class RunRepository(AbstractRepository[Run, int]):
    def save(self, run: Run) -> Run:
        raise NotImplementedError()

    def find_by_id(self, id: int) -> Optional[Run]:
        pass
