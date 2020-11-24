from cato.domain.project import Project
from cato.storage.abstract.abstract_repository import AbstractRepository


class ProjectRepository(AbstractRepository[Project, int]):
    def save(self, project: Project) -> Project:
        raise NotImplementedError()

    def find_by_name(self, name: str) -> Project:
        raise NotImplementedError()
