from sqlalchemy import Column, Integer, ForeignKey, String, JSON

from cato.storage.abstract.suite_result_repository import SuiteResultRepository
from cato.storage.domain.suite_result import SuiteResult
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _SuiteResultMapping(Base):
    __tablename__ = "suite_result_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_entity_id = Column(Integer, ForeignKey("run_entity.id"))
    suite_name = Column(String, nullable=False)
    suite_variables = Column(JSON, nullable=False)


class SqlAlchemySuiteResultRepository(
    AbstractSqlAlchemyRepository, SuiteResultRepository
):
    def to_entity(self, domain_object: SuiteResult) -> _SuiteResultMapping:
        return _SuiteResultMapping(
            id=domain_object.id if domain_object.id else None,
            run_entity_id=domain_object.run_id,
            suite_name=domain_object.suite_name,
            suite_variables=domain_object.suite_variables,
        )

    def to_domain_object(self, entity: _SuiteResultMapping) -> SuiteResult:
        return SuiteResult(
            id=entity.id,
            run_id=entity.run_entity_id,
            suite_name=entity.suite_name,
            suite_variables=entity.suite_variables,
        )

    def mapping_cls(self):
        return _SuiteResultMapping
