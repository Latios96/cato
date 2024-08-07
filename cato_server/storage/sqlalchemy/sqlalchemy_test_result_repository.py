import dataclasses
from collections import defaultdict
from typing import Optional, Set, Dict, List

from sqlalchemy import Column, String, Integer, ForeignKey, JSON, Float, func
from cato_server.storage.sqlalchemy.type_decorators.utc_date_time import UtcDateTime

from cato_common.domain.comparison_method import ComparisonMethod
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.machine_info import MachineInfo
from cato_common.domain.test_failure_reason import TestFailureReason
from cato_common.domain.test_identifier import TestIdentifier
from cato_common.domain.test_result import TestResult
from cato_common.domain.unified_test_status import UnifiedTestStatus
from cato_common.storage.page import PageRequest, Page
from cato_server.domain.test_result_status_information import (
    TestResultStatusInformation,
)
from cato_server.storage.abstract.status_filter import StatusFilter
from cato_server.storage.abstract.test_result_filter_options import (
    TestResultFilterOptions,
)
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
from cato_common.utils.datetime_utils import aware_now_in_utc


class _TestResultMapping(Base):
    __tablename__ = "test_result_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    suite_result_entity_id = Column(Integer, ForeignKey("suite_result_entity.id"))
    test_name = Column(String, nullable=False)
    test_identifier = Column(String, nullable=False)
    test_command = Column(String, nullable=False)
    test_variables = Column(JSON, nullable=False)
    machine_info = Column(JSON, nullable=True)
    unified_test_status = Column(String, nullable=False)
    seconds = Column(Float, nullable=True)
    message = Column(String, nullable=True)
    image_output_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    reference_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    started_at = Column(UtcDateTime, nullable=True)
    finished_at = Column(UtcDateTime, nullable=True)
    comparison_settings_method = Column(String, nullable=True)
    comparison_settings_threshold = Column(Float, nullable=True)
    error_value = Column(Float, nullable=True)
    thumbnail_file_entity_id = Column(
        Integer, ForeignKey("file_entity.id"), nullable=True
    )
    failure_reason = Column(String, nullable=True)
    # deprecated, only there for migrations
    # execution_status = Column(String, nullable=True)
    # status = Column(String, nullable=True)

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
            machine_info=(
                dataclasses.asdict(domain_object.machine_info)
                if domain_object.machine_info
                else None
            ),
            unified_test_status=domain_object.unified_test_status.name,
            seconds=domain_object.seconds,
            message=domain_object.message,
            image_output_id=domain_object.image_output,
            reference_image_id=domain_object.reference_image,
            diff_image_id=domain_object.diff_image,
            started_at=domain_object.started_at,
            finished_at=domain_object.finished_at,
            comparison_settings_method=(
                domain_object.comparison_settings.method.value
                if domain_object.comparison_settings
                else None
            ),
            comparison_settings_threshold=(
                domain_object.comparison_settings.threshold
                if domain_object.comparison_settings
                else None
            ),
            error_value=domain_object.error_value,
            thumbnail_file_entity_id=domain_object.thumbnail_file_id,
            failure_reason=(
                domain_object.failure_reason.name
                if domain_object.failure_reason
                else None
            ),
        )

    def to_domain_object(self, entity: _TestResultMapping) -> TestResult:
        return TestResult(
            id=entity.id,
            suite_result_id=entity.suite_result_entity_id,
            test_name=entity.test_name,
            test_identifier=TestIdentifier.from_string(entity.test_identifier),
            test_command=entity.test_command,
            test_variables=entity.test_variables,
            machine_info=(
                MachineInfo(
                    cpu_name=entity.machine_info["cpu_name"],
                    cores=entity.machine_info["cores"],
                    memory=entity.machine_info["memory"],
                )
                if entity.machine_info
                else None
            ),
            unified_test_status=UnifiedTestStatus(entity.unified_test_status),
            seconds=entity.seconds,
            message=entity.message,
            image_output=entity.image_output_id,
            reference_image=entity.reference_image_id,
            diff_image=entity.diff_image_id,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
            comparison_settings=(
                ComparisonSettings(
                    method=ComparisonMethod(entity.comparison_settings_method),
                    threshold=entity.comparison_settings_threshold,
                )
                if entity.comparison_settings_method
                else None
            ),
            error_value=entity.error_value,
            thumbnail_file_id=entity.thumbnail_file_entity_id,
            failure_reason=(
                TestFailureReason(entity.failure_reason)
                if entity.failure_reason
                else None
            ),
        )

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

    def find_by_run_id(
        self, run_id: int, filter_options: Optional[TestResultFilterOptions] = None
    ) -> List[TestResult]:
        session = self._session_maker()

        query = (
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
        )
        query = self._add_filter_options(filter_options, query)
        entities = self._order_by_case_insensitive(
            query,
            self.mapping_cls().test_identifier,
        ).all()
        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id_with_paging(
        self,
        run_id: int,
        page_request: PageRequest,
        filter_options: Optional[TestResultFilterOptions] = None,
    ) -> Page[TestResult]:
        session = self._session_maker()

        page = self._pageginate(
            session,
            self._order_by_case_insensitive(
                self._add_filter_options(
                    filter_options,
                    session.query(_TestResultMapping)
                    .join(_SuiteResultMapping)
                    .join(_RunMapping)
                    .filter(_RunMapping.id == run_id),
                ),
                self.mapping_cls().test_identifier,
            ),
            page_request,
        )
        session.close()
        return page

    def find_status_by_run_ids(
        self, run_ids: Set[int]
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.unified_test_status,
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
        for unified_test_status, run_id in results:
            status_by_run_id[run_id].add(unified_test_status)

        return status_by_run_id

    def find_status_by_project_id(
        self, project_id: int
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.unified_test_status,
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
        for unified_test_status, run_id in results:
            status_by_run_id[run_id].add(unified_test_status)

        return status_by_run_id

    def test_count_by_run_ids(self, run_ids: Set[int]) -> Dict[int, int]:
        with self._session_maker() as session:
            test_result_counts = (
                session.query(
                    func.count(_TestResultMapping.id),
                    _RunMapping.id,
                )
                .join(_SuiteResultMapping.test_results)
                .join(_RunMapping)
                .filter(_RunMapping.id.in_(run_ids))
                .group_by(_RunMapping.id)
                .all()
            )
            counts_by_run_id = defaultdict(lambda: 0)
            counts_by_run_id.update(
                {
                    run_id: suite_result_count
                    for suite_result_count, run_id in test_result_counts
                }
            )
            return counts_by_run_id

    def duration_by_run_ids(self, run_ids: Set[int]) -> Dict[int, float]:
        session = self._session_maker()

        summed_durations = (
            session.query(_RunMapping.id, func.sum(_TestResultMapping.seconds))
            .select_from(_RunMapping)
            .join(_SuiteResultMapping)
            .join(_TestResultMapping)
            .filter(_RunMapping.id.in_(run_ids))
            .group_by(_RunMapping.id)
            .all()
        )
        summed_durations = {id: duration for id, duration in summed_durations}

        start_points_of_started_tests = (
            session.query(_RunMapping.id, _TestResultMapping.started_at)
            .select_from(_RunMapping)
            .join(_SuiteResultMapping)
            .join(_TestResultMapping)
            .filter(_RunMapping.id.in_(run_ids))
            .filter(_TestResultMapping.unified_test_status == "RUNNING")
            .all()
        )
        now = aware_now_in_utc()
        additional_durations = {
            id: (now - started_at).seconds
            for id, started_at in start_points_of_started_tests
        }

        for run_id in run_ids:
            has_duration_for_running_tests = (
                additional_durations.get(run_id) is not None
            )
            has_duration_for_finished_tests = summed_durations.get(run_id) is not None
            if has_duration_for_finished_tests and has_duration_for_running_tests:
                summed_durations[run_id] += additional_durations[run_id]
            elif summed_durations.get(run_id) is None:
                summed_durations[run_id] = 0

        session.close()

        return summed_durations

    def find_status_by_suite_ids(
        self, suite_ids: Set[int]
    ) -> Dict[int, Set[UnifiedTestStatus]]:
        session = self._session_maker()

        results = (
            session.query(
                _TestResultMapping.unified_test_status,
                _SuiteResultMapping.id,
            )
            .distinct()
            .join(_SuiteResultMapping.test_results)
            .filter(_SuiteResultMapping.id.in_(suite_ids))
            .all()
        )
        session.close()
        status_by_run_id = defaultdict(set)
        for unified_test_status, run_id in results:
            status_by_run_id[run_id].add(unified_test_status)

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
        self, run_id: int, test_status: UnifiedTestStatus
    ) -> List[TestResult]:
        session = self._session_maker()

        entities = self._order_by_case_insensitive(
            session.query(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .filter(_TestResultMapping.unified_test_status == test_status.value),
            self.mapping_cls().test_name,
        ).all()
        session.close()

        return self._map_many_to_domain_object(entities)

    def status_information_by_run_ids(
        self, run_ids: Set[int]
    ) -> Dict[int, TestResultStatusInformation]:
        with self._session_maker() as session:
            unified_status_counts = (
                session.query(
                    _TestResultMapping.unified_test_status,
                    func.count(_TestResultMapping.unified_test_status),
                    _RunMapping.id,
                )
                .select_from(_TestResultMapping)
                .join(_SuiteResultMapping)
                .join(_RunMapping)
                .filter(_RunMapping.id.in_(run_ids))
                .group_by(_TestResultMapping.unified_test_status)
                .group_by(_RunMapping.id)
                .all()
            )

            return self.__status_count_query_result_to_dict(unified_status_counts)

    def __status_count_query_result_to_dict(self, unified_status_counts):
        status_counts_by_run_id = defaultdict(
            lambda: TestResultStatusInformation(
                not_started=0,
                running=0,
                failed=0,
                success=0,
            )
        )

        for (
            unified_test_status,
            unified_test_status_count,
            run_id,
        ) in unified_status_counts:
            if unified_test_status == "NOT_STARTED":
                status_counts_by_run_id[run_id].not_started = unified_test_status_count
            elif unified_test_status == "RUNNING":
                status_counts_by_run_id[run_id].running = unified_test_status_count
            elif unified_test_status == "FAILED":
                status_counts_by_run_id[run_id].failed = unified_test_status_count
            elif unified_test_status == "SUCCESS":
                status_counts_by_run_id[run_id].success = unified_test_status_count

        return status_counts_by_run_id

    def _add_filter_options(self, filter_options: TestResultFilterOptions, query):
        if filter_options and filter_options.status is not StatusFilter.NONE:
            query = query.filter(
                _TestResultMapping.unified_test_status == filter_options.status.value
            )

            if filter_options.failure_reason:
                query = query.filter(
                    _TestResultMapping.failure_reason
                    == filter_options.failure_reason.value
                )
        return query
