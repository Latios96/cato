from typing import Optional

from sqlalchemy import Column, Integer, Text

from cato_server.domain.auth.auth_user import AuthUser
from cato_common.domain.auth.email import Email
from cato_common.domain.auth.username import Username
from cato_server.storage.abstract.auth_user_repository import (
    AuthUserRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _AuthUserMapping(Base):
    __tablename__ = "user_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    fullname = Column(Text, nullable=False)
    email = Column(Text, nullable=False)


class SqlAlchemyAuthUserRepository(
    AbstractSqlAlchemyRepository[AuthUser, _AuthUserMapping, int],
    AuthUserRepository,
):
    def to_entity(self, domain_object: AuthUser) -> _AuthUserMapping:
        return _AuthUserMapping(
            id=domain_object.id if domain_object.id else None,
            username=str(domain_object.username),
            fullname=str(domain_object.fullname),
            email=str(domain_object.email),
        )

    def to_domain_object(self, entity: _AuthUserMapping) -> AuthUser:
        return AuthUser(
            id=entity.id,
            username=Username(entity.username),
            fullname=Username(entity.fullname),
            email=Email(entity.email),
        )

    def find_by_username(self, username: Username) -> Optional[AuthUser]:
        with self._session_maker() as session:
            query = session.query(self.mapping_cls()).filter(
                self.mapping_cls().username == str(username)
            )
            return self._map_one_to_domain_object(query.first())

    def find_by_email(self, email: Email) -> Optional[AuthUser]:
        with self._session_maker() as session:
            query = session.query(self.mapping_cls()).filter(
                self.mapping_cls().email == str(email)
            )
            return self._map_one_to_domain_object(query.first())

    def exists_by_username(self, username: Username) -> bool:
        with self._session_maker() as session:
            query = session.query(self.mapping_cls()).filter(
                self.mapping_cls().username == str(username)
            )
            return session.query(query.exists()).scalar()

    def exists_by_email(self, email: Email) -> bool:
        with self._session_maker() as session:
            query = session.query(self.mapping_cls()).filter(
                self.mapping_cls().email == str(email)
            )
            return session.query(query.exists()).scalar()

    def mapping_cls(self):
        return _AuthUserMapping
