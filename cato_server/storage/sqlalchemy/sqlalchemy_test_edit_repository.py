from typing import Optional, List

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, JSON

from cato_server.domain.test_edit import TestEdit, EditTypes
from cato_server.storage.abstract.test_edit_repository import TestEditRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    Base,
    AbstractSqlAlchemyRepository,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import _RunMapping
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    _SuiteResultMapping,
)
from cato_server.storage.sqlalchemy.sqlalchemy_test_result_repository import (
    _TestResultMapping,
)


class _TestEditMapping(Base):
    __tablename__ = "test_edit_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey("test_result_entity.id"), nullable=False)
    edit_type = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    old_value = Column(JSON, nullable=False)
    new_value = Column(JSON, nullable=False)


class SqlAlchemyTestEditRepository(AbstractSqlAlchemyRepository, TestEditRepository):
    def to_entity(self, domain_object: TestEdit) -> _TestEditMapping:
        return _TestEditMapping(
            id=domain_object.id if domain_object.id else None,
            test_id=domain_object.test_id,
            edit_type=domain_object.edit_type.value,
            created_at=domain_object.created_at,
            old_value=domain_object.old_value,
            new_value=domain_object.new_value,
        )

    def to_domain_object(self, entity: _TestEditMapping) -> TestEdit:
        return TestEdit(
            id=entity.id,
            test_id=entity.test_id,
            edit_type=EditTypes(entity.edit_type),
            created_at=entity.created_at,
            old_value=entity.old_value,
            new_value=entity.new_value,
        )

    def mapping_cls(self):
        return _TestEditMapping

    def find_by_test_id(
        self, test_id: int, edit_type: Optional[EditTypes] = None
    ) -> List[TestEdit]:
        session = self._session_maker()

        query = session.query(self.mapping_cls()).filter(
            self.mapping_cls().test_id == test_id
        )

        if edit_type is not None:
            query = query.filter(self.mapping_cls().edit_type == edit_type.value)

        entities = query.order_by(self.mapping_cls().created_at.desc()).all()

        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id(self, run_id: int) -> List[TestEdit]:
        session = self._session_maker()

        entities = (
            session.query(_TestEditMapping)
            .join(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .order_by(self.mapping_cls().created_at.desc())
            .all
        )

        session.close()
        return list(map(self.to_domain_object, entities))
