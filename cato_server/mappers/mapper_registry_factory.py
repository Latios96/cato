from cato_server.domain.project import Project
from cato_server.mappers.mapper_registry import MapperRegistry
from cato_server.mappers.project_class_mapper import ProjectClassMapper


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()

        mapper_registry.register_mapper(Project, ProjectClassMapper())

        return mapper_registry
