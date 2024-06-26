from typing import Optional

from cato_common.domain.project import Project
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class ProjectRepository(AbstractRepository[Project, int]):
    def find_by_name(self, name: str) -> Optional[Project]:
        raise NotImplementedError()
