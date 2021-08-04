import datetime

from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.mappers.internal.datetime_value_mapper import DateTimeValueMapper
from cato_server.mappers.internal.test_identifier_value_mapper import (
    TestIdentifierValueMapper,
)
from cato_server.mappers.internal.test_result_class_mapper import TestResultClassMapper
from cato_server.mappers.mapper_registry import MapperRegistry


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()
        mapper_registry.register_value_mapper(
            TestIdentifier, TestIdentifierValueMapper()
        )
        mapper_registry.register_value_mapper(datetime.datetime, DateTimeValueMapper())

        mapper_registry.register_class_mapper(TestResult, TestResultClassMapper())

        return mapper_registry
