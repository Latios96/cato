from typing import Optional

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float, DateTime
from sqlalchemy.orm import relationship

from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_result import TestStatus
from cato.storage.abstract.abstract_test_result_repository import (
    TestResultRepository,
)
from cato.storage.domain.test_result import TestResult
from cato.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _TestResultMapping(Base):
    __tablename__ = "test_result_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    suite_result_entity_id = Column(Integer, ForeignKey("suite_result_entity.id"))
    test_name = Column(String, nullable=False)
    test_identifier = Column(String, nullable=False)
    test_command = Column(String, nullable=False)
    test_variables = Column(JSON, nullable=False)
    execution_status = Column(String, nullable=True)
    status = Column(String, nullable=True)
    output = Column(JSON, nullable=False)
    seconds = Column(Float, nullable=False)
    message = Column(String, nullable=True)
    image_output = Column(String, nullable=True)
    reference_image = Column(String, nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)


class SqlAlchemyTestResultRepository(
    AbstractSqlAlchemyRepository, TestResultRepository
):
    def to_entity(self, domain_object: TestResult) -> _TestResultMapping:
        return _TestResultMapping(
            id=domain_object.id if domain_object.id else None,
            suite_result_entity_id=domain_object.suite_result_id,
            test_name=domain_object.test_name,
            test_identifier=str(domain_object.test_identifier),
            test_command=domain_object.test_command,
            test_variables=domain_object.test_variables,
            execution_status=domain_object.execution_status,
            status=domain_object.status.name if domain_object.status else None,
            output=domain_object.output,
            seconds=domain_object.seconds,
            message=domain_object.message,
            image_output=domain_object.image_output,
            reference_image=domain_object.reference_image,
            started_at=domain_object.started_at,
            finished_at=domain_object.finished_at,
        )

    def to_domain_object(self, entity: _TestResultMapping) -> TestResult:
        return TestResult(
            id=entity.id,
            suite_result_id=entity.suite_result_entity_id,
            test_name=entity.test_name,
            test_identifier=TestIdentifier.from_string(entity.test_identifier),
            test_command=entity.test_command,
            test_variables=entity.test_variables,
            execution_status=entity.execution_status,
            status=self._map_test_status(entity.status),
            output=entity.output,
            seconds=entity.seconds,
            message=entity.message,
            image_output=entity.image_output,
            reference_image=entity.reference_image,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
        )

    def _map_test_status(self, status):
        if not status:
            return None
        return TestStatus.SUCCESS if status == "SUCCESS" else TestStatus.FAILED

    def mapping_cls(self):
        return _TestResultMapping

    def find_by_suite_result_and_test_identifier(
        self, suite_result_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        session = self._session_maker()

        entity = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().suite_result_entity_id == suite_result_id)
            .filter(self.mapping_cls().test_identifier == str(test_identifier))
            .first()
        )
        if entity:
            return self.to_domain_object(entity)
