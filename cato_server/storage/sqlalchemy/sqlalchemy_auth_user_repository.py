from sqlalchemy import Column, Integer, Text

from cato_server.domain.auth_user import AuthUser
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _AuthUserMapping(Base):
    __tablename__ = "user_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    hashed_password = Column(Text, nullable=False)


class SqlAlchemyAuthUserRepository(
    AbstractSqlAlchemyRepository[AuthUser, _AuthUserMapping, int]
):
    def to_entity(self, domain_object: AuthUser) -> _AuthUserMapping:
        return _AuthUserMapping(
            id=domain_object.id if domain_object.id else None,
            username=domain_object.username,
            hashed_password=domain_object.hashed_password,
        )

    def to_domain_object(self, entity: _AuthUserMapping) -> AuthUser:
        return AuthUser(
            id=entity.id,
            username=entity.username,
            hashed_password=entity.hashed_password,
        )

    def mapping_cls(self):
        return _AuthUserMapping
