from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_common.domain.branch_name import BranchName
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.mappers.internal.branch_name_value_mapper import BranchNameValueMapper
from cato_common.mappers.internal.email_value_mapper import EmailValueMapper
from cato_common.mappers.internal.test_identifier_value_mapper import (
    TestIdentifierValueMapper,
)
from cato_common.mappers.internal.username_value_mapper import UsernameValueMapper
from cato_common.mappers.mapper_registry import MapperRegistry


class MapperRegistryFactory:
    def create_mapper_registry(self) -> MapperRegistry:
        mapper_registry = MapperRegistry()
        mapper_registry.register_value_mapper(
            TestIdentifier, TestIdentifierValueMapper()
        )
        mapper_registry.register_value_mapper(BranchName, BranchNameValueMapper())
        mapper_registry.register_value_mapper(Username, UsernameValueMapper())
        mapper_registry.register_value_mapper(Email, EmailValueMapper())

        return mapper_registry
