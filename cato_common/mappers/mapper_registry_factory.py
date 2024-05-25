from cato_common.domain.auth.api_token_id import ApiTokenId
from cato_common.domain.auth.api_token_name import ApiTokenName
from cato_common.domain.auth.api_token_str import ApiTokenStr
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_common.domain.branch_name import BranchName
from cato_common.domain.run_identifier import RunIdentifier
from cato_common.domain.run_name import RunName
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.mappers.internal.api_token_id_mapper import ApiTokenIdValueMapper
from cato_common.mappers.internal.api_token_name_mapper import ApiTokenNameValueMapper
from cato_common.mappers.internal.api_token_str_mapper import ApiTokenStrValueMapper
from cato_common.mappers.internal.branch_name_value_mapper import BranchNameValueMapper
from cato_common.mappers.internal.email_value_mapper import EmailValueMapper
from cato_common.mappers.internal.run_identifier_mapper import RunIdentifierValueMapper
from cato_common.mappers.internal.run_name_mapper import RunNameValueMapper
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
        mapper_registry.register_value_mapper(ApiTokenId, ApiTokenIdValueMapper())
        mapper_registry.register_value_mapper(ApiTokenName, ApiTokenNameValueMapper())
        mapper_registry.register_value_mapper(ApiTokenStr, ApiTokenStrValueMapper())
        mapper_registry.register_value_mapper(RunIdentifier, RunIdentifierValueMapper())
        mapper_registry.register_value_mapper(RunName, RunNameValueMapper())

        return mapper_registry
