import dataclasses
from collections import defaultdict
import datetime
from typing import Optional, Set, Tuple, Dict, List

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float, DateTime, func

from cato.domain.test_status import TestStatus
from cato_server.domain.execution_status import ExecutionStatus
from cato_server.domain.machine_info import MachineInfo
from cato_server.domain.test_identifier import TestIdentifier
from cato_server.domain.test_result import TestResult
from cato_server.storage.abstract.page import PageRequest, Page
from cato_server.storage.abstract.test_result_repository import (
    TestResultRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)
from cato_server.storage.sqlalchemy.sqlalchemy_run_repository import _RunMapping
from cato_server.storage.sqlalchemy.sqlalchemy_suite_result_repository import (
    _SuiteResultMapping,
)


class _TestResultMapping(Base):
    __tablename__ = "test_result_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    suite_result_entity_id = Column(Integer, ForeignKey("suite_result_entity.id"))
    test_name = Column(String, nullable=False)
    test_identifier = Column(String, nullable=False)
    test_command = Column(String, nullable=False)
    test_variables = Column(JSON, nullable=False)
    machine_info = Column(JSON, nullable=True)
    execution_status = Column(String, nullable=True)
    status = Column(String, nullable=True)
    seconds = Column(Float, nullable=False)
    message = Column(String, nullable=True)
    image_output_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    reference_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    started_at = Column(DateTime, nullable=True)
    finished_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<_TestResultMapping id={self.id}>"


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
            machine_info=dataclasses.asdict(domain_object.machine_info)
            if domain_object.machine_info
            else None,
            execution_status=domain_object.execution_status.name
            if domain_object.execution_status
            else None,
            status=domain_object.status.name if domain_object.status else None,
            seconds=domain_object.seconds,
            message=domain_object.message,
            image_output_id=domain_object.image_output,
            reference_image_id=domain_object.reference_image,
            diff_image_id=domain_object.diff_image,
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
            machine_info=MachineInfo(
                cpu_name=entity.machine_info["cpu_name"],
                cores=entity.machine_info["cores"],
                memory=entity.machine_info["memory"],
            )
            if entity.machine_info
            else None,
            execution_status=self._map_execution_status(entity.execution_status),
            status=self._map_test_status(entity.status),
            seconds=entity.seconds,
            message=entity.message,
            image_output=entity.image_output_id,
            reference_image=entity.reference_image_id,
            diff_image=entity.diff_image_id,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
        )

    def _map_test_status(self, status):
        if not status:
            return None
        return TestStatus.SUCCESS if status == "SUCCESS" else TestStatus.FAILED

    def _map_execution_status(self, status):
        if not status:
            return None
        return {
            "NOT_STARTED": ExecutionStatus.NOT_STARTED,
            "RUNNING": ExecutionStatus.RUNNING,
            "FINISHED": ExecutionStatus.FINISHED,
        }[status]

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
        session.close()
        if entity:
            return self.to_domain_object(entity)

    def find_by_suite_result_id(self, suite_result_id: int) -> List[TestResult]:
        session = self._session_maker()

        entities = (
            session.query(self.mapping_cls())
            .filter(self.mapping_cls().suite_result_entity_id == suite_result_id)
            .all()
        )
        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id(self, run_id: int) -> List[TestResult]:
        session = self._session_maker()

        entities = self._order_by_case_insensitive(
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id),
            self.mapping_cls().test_name,
        ).all()
        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id_with_paging(
        self, run_id: int, page_request: PageRequest
    ) -> Page[TestResult]:
        session = self._session_maker()

        page = self._pageginate(
            session,
            self._order_by_case_insensitive(
                session.query(_TestResultMapping)
                .join(_SuiteResultMapping)
                .join(_RunMapping)
                .filter(_RunMapping.id == run_id),
                self.mapping_cls().test_identifier,
            ),
            page_request,
        )
        session.close()
        return page

    def find_execution_status_by_run_ids(
        self, run_ids: Set[int]
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.execution_status,
                _TestResultMapping.status,
                _RunMapping.id,
            )
            .distinct()
            .join(_SuiteResultMapping.test_results)
            .join(_RunMapping)
            .filter(_RunMapping.id.in_(run_ids))
            .all()
        )
        session.close()
        status_by_run_id = defaultdict(set)
        for execution_status, test_status, run_id in results:
            status_by_run_id[run_id].add(
                (
                    self._map_execution_status(execution_status),
                    self._map_test_status(test_status),
                )
            )

        return status_by_run_id

    def find_execution_status_by_project_id(
        self, project_id: int
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.execution_status,
                _TestResultMapping.status,
                _RunMapping.id,
            )
            .distinct()
            .join(_SuiteResultMapping.test_results)
            .join(_RunMapping)
            .filter(_RunMapping.project_entity_id == project_id)
            .all()
        )
        session.close()
        status_by_run_id = defaultdict(set)
        for execution_status, test_status, run_id in results:
            status_by_run_id[run_id].add(
                (
                    self._map_execution_status(execution_status),
                    self._map_test_status(test_status),
                )
            )

        return status_by_run_id

    def test_count_by_run_id(self, run_id: int) -> int:
        session = self._session_maker()

        count = (
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .count()
        )
        session.close()
        return count

    def failed_test_count_by_run_id(self, run_id: int) -> int:
        session = self._session_maker()

        count = (
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .filter(_TestResultMapping.status == "FAILED")
            .count()
        )
        session.close()
        return count

    def duration_by_run_id(self, run_id: int) -> float:
        session = self._session_maker()

        summed_duration = (
            session.query(func.sum(_TestResultMapping.seconds).label("duration"))
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .scalar()
        )
        summed_duration = summed_duration if summed_duration is not None else 0

        start_points_of_started_tests = (
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .filter(_TestResultMapping.execution_status == "RUNNING")
            .all()
        )
        now = datetime.datetime.now()
        additional_durations = list(
            map(lambda x: (now - x.started_at).seconds, start_points_of_started_tests)
        )

        total_duration = summed_duration + sum(additional_durations)

        session.close()
        return total_duration

    def find_execution_status_by_suite_ids(
        self, suite_ids: Set[int]
    ) -> Dict[int, Set[Tuple[ExecutionStatus, TestStatus]]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.execution_status,
                _TestResultMapping.status,
                _SuiteResultMapping.id,
            )
            .distinct()
            .join(_SuiteResultMapping.test_results)
            .filter(_SuiteResultMapping.id.in_(suite_ids))
            .all()
        )
        session.close()
        status_by_run_id = defaultdict(set)
        for execution_status, test_status, run_id in results:
            status_by_run_id[run_id].add(
                (
                    self._map_execution_status(execution_status),
                    self._map_test_status(test_status),
                )
            )

        return status_by_run_id

    def find_by_run_id_and_test_identifier(
        self, run_id: int, test_identifier: TestIdentifier
    ) -> Optional[TestResult]:
        session = self._session_maker()

        entity = (
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .filter(_TestResultMapping.test_identifier == str(test_identifier))
            .first()
        )
        session.close()
        if entity:
            return self.to_domain_object(entity)

    def find_by_run_id_filter_by_test_status(
        self, run_id: int, test_status: TestStatus
    ) -> List[TestResult]:
        session = self._session_maker()

        entities = self._order_by_case_insensitive(
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .filter(_TestResultMapping.status == self._map_test_status(test_status)),
            self.mapping_cls().test_name,
        ).all()
        session.close()

        return self._map_many_to_domain_object(entities)
