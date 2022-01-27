from typing import Optional

from sqlalchemy import Column, Integer, Text

from cato_server.domain.auth.auth_user import AuthUser
from cato_server.storage.abstract.abstract_auth_user_repository import (
    AbstractAuthUserRepository,
)
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
    AbstractSqlAlchemyRepository[AuthUser, _AuthUserMapping, int],
    AbstractAuthUserRepository,
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

    def find_by_username(self, username: str) -> Optional[AuthUser]:
        session = self._session_maker()

        query = session.query(self.mapping_cls()).filter(
            self.mapping_cls().username == username
        )
        session.close()
        return self._map_one_to_domain_object(query.first())

    def mapping_cls(self):
        return _AuthUserMapping
