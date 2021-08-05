from cato_common.domain.test_identifier import TestIdentifier
from cato_server.mappers.internal.test_identifier_value_mapper import (
    TestIdentifierValueMapper,
)
from cato_server.mappers.mapper_registry import MapperRegistry


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()
        mapper_registry.register_value_mapper(
            TestIdentifier, TestIdentifierValueMapper()
        )

        return mapper_registry
