from typing import List, Optional, cast

from sqlalchemy import Column, Integer, ForeignKey, String, BigInteger
from sqlalchemy.orm import relationship, with_polymorphic, joinedload

from cato_common.domain.branch_name import BranchName
from cato_common.domain.run import (
    Run,
)
from cato_common.domain.run_information import (
    OS,
    BasicRunInformation,
    LocalComputerRunInformation,
    GithubActionsRunInformation,
)
from cato_common.domain.run_batch_provider import RunBatchProvider
from cato_common.storage.page import PageRequest, Page
from cato_server.storage.abstract.run_filter_options import RunFilterOptions
from cato_server.storage.abstract.run_repository import RunRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)
from cato_server.storage.sqlalchemy.type_decorators.utc_date_time import UtcDateTime


class _BasicRunInformationMapping(Base):
    __tablename__ = "basic_run_information_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_entity_id = Column(Integer, ForeignKey("run_entity.id"), nullable=False)
    run_information_type = Column(String, nullable=False)
    os = Column(String, nullable=False)
    computer_name = Column(String, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": "run_information_type",
        "polymorphic_on": run_information_type,
    }

    run = relationship("_RunMapping", back_populates="run_information")


class _LocalComputerRunInformationMapping(_BasicRunInformationMapping):
    __tablename__ = "local_computer_run_information_entity"

    id = Column(
        Integer, ForeignKey("basic_run_information_entity.id"), primary_key=True
    )
    local_username = Column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": RunBatchProvider.LOCAL_COMPUTER.value}


class _GithubActionsRunInformationMapping(_BasicRunInformationMapping):
    __tablename__ = "github_actions_run_information_entity"

    id = Column(
        Integer, ForeignKey("basic_run_information_entity.id"), primary_key=True
    )
    github_run_id = Column(BigInteger, nullable=False)
    html_url = Column(String, nullable=False)
    job_name = Column(String, nullable=False)
    actor = Column(String, nullable=False)
    attempt = Column(Integer, nullable=False)
    run_number = Column(Integer, nullable=False)
    github_url = Column(String, nullable=False)
    github_api_url = Column(String, nullable=False)

    __mapper_args__ = {"polymorphic_identity": RunBatchProvider.GITHUB_ACTIONS.value}


class _RunMapping(Base):
    __tablename__ = "run_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_entity_id = Column(Integer, ForeignKey("project_entity.id"))
    run_batch_entity_id = Column(Integer, ForeignKey("run_batch_entity.id"))
    created_at = Column(UtcDateTime)
    branch_name = Column(String, nullable=False)
    previous_run_id = Column(Integer, ForeignKey("run_entity.id"), nullable=True)
    performance_trace_entity_id = Column(
        Integer, ForeignKey("performance_trace_entity.id"), nullable=True
    )

    run_information = relationship(
        _BasicRunInformationMapping,
        uselist=False,
        back_populates="run",
        cascade="all, delete",
    )


class SqlAlchemyRunRepository(AbstractSqlAlchemyRepository, RunRepository):
    def to_entity(self, domain_object: Run) -> _RunMapping:
        return SqlAlchemyRunRepository.static_to_entity(domain_object)

    @staticmethod
    def static_to_entity(domain_object: Run) -> _RunMapping:
        return _RunMapping(
            id=domain_object.id if domain_object.id else None,
            project_entity_id=domain_object.project_id,
            run_batch_entity_id=domain_object.run_batch_id,
            created_at=domain_object.created_at,
            branch_name=str(domain_object.branch_name),
            previous_run_id=domain_object.previous_run_id,
            run_information=SqlAlchemyRunRepository._run_information_to_entity(
                domain_object.run_information
            ),
            performance_trace_entity_id=domain_object.performance_trace_id,
        )

    def to_domain_object(self, entity: _RunMapping) -> Run:
        return SqlAlchemyRunRepository.static_to_domain_object(entity)

    @staticmethod
    def static_to_domain_object(entity: _RunMapping) -> Run:
        return Run(
            id=entity.id,
            project_id=entity.project_entity_id,
            run_batch_id=entity.run_batch_entity_id,
            created_at=entity.created_at,
            branch_name=BranchName(entity.branch_name),
            previous_run_id=entity.previous_run_id,
            run_information=SqlAlchemyRunRepository._run_information_to_domain_object(
                entity.run_information
            ),
            performance_trace_id=entity.performance_trace_entity_id,
        )

    def insert_many(self, domain_objects: List[Run]) -> List[Run]:
        with self._session_maker() as session:
            mapped_entities = list(map(self.to_entity, domain_objects))

            session.add_all(mapped_entities)

            session.flush()
            session.commit()

            domain_objects = list(map(self.to_domain_object, mapped_entities))

            return domain_objects

    def mapping_cls(self):
        return _RunMapping

    def default_query_options(self):
        return [
            joinedload(
                _RunMapping.run_information.of_type(
                    with_polymorphic(
                        _BasicRunInformationMapping,
                        [
                            _LocalComputerRunInformationMapping,
                            _GithubActionsRunInformationMapping,
                        ],
                        flat=True,
                    )
                )
            )
        ]

    def find_by_project_id(self, id: int) -> List[Run]:
        with self._session_maker() as session:
            entities = (
                session.query(self.mapping_cls())
                .filter(self.mapping_cls().project_entity_id == id)
                .order_by(self.mapping_cls().created_at.desc())
                .order_by(self.mapping_cls().id.desc())
                .options(self.default_query_options())
                .all()
            )

            return list(map(self.to_domain_object, entities))

    def find_by_project_id_with_paging(
        self,
        id: int,
        page_request: PageRequest,
        filter_options: Optional[RunFilterOptions] = None,
    ) -> Page[Run]:
        session = self._session_maker()

        query = (
            session.query(self.mapping_cls())
            .join(_BasicRunInformationMapping)
            .filter(self.mapping_cls().project_entity_id == id)
            .options(self.default_query_options())
        )
        if filter_options:
            query = self._apply_filter_options(query, filter_options)
        page = self._pageginate(
            session,
            query.order_by(self.mapping_cls().created_at.desc()).order_by(
                self.mapping_cls().id.desc()
            ),
            page_request,
        )

        session.close()
        return page

    def find_last_run_for_project(
        self, project_id: int, branch_name: BranchName
    ) -> Optional[Run]:
        with self._session_maker() as session:
            query = (
                session.query(_RunMapping)
                .filter(_RunMapping.project_entity_id == project_id)
                .filter(_RunMapping.branch_name == branch_name.name)
                .order_by(_RunMapping.id.desc())
            )
            return self._map_one_to_domain_object(query.first())

    def _apply_filter_options(self, query, filter_options: RunFilterOptions):
        return query.filter(
            self.mapping_cls().branch_name.in_(
                {x.name for x in filter_options.branches}
            )
        )

    def find_branches_for_project(self, project_id: int) -> List[BranchName]:
        session = self._session_maker()

        query = (
            session.query(_RunMapping.branch_name)
            .distinct()
            .filter(_RunMapping.project_entity_id == project_id)
        )
        query = self._order_by_case_insensitive(query, _RunMapping.branch_name)
        branch_names = query.all()
        session.close()

        return [BranchName(x[0]) for x in branch_names]

    @staticmethod
    def _run_information_to_entity(run_information: BasicRunInformation):
        if run_information.run_information_type == RunBatchProvider.LOCAL_COMPUTER:
            run_information = cast(LocalComputerRunInformation, run_information)
            return _LocalComputerRunInformationMapping(
                id=run_information.id if run_information.id else None,
                run_entity_id=run_information.run_id,
                run_information_type=run_information.run_information_type.value,
                os=run_information.os.name,
                computer_name=run_information.computer_name,
                local_username=run_information.local_username,
            )
        elif run_information.run_information_type == RunBatchProvider.GITHUB_ACTIONS:
            run_information = cast(GithubActionsRunInformation, run_information)
            return _GithubActionsRunInformationMapping(
                id=run_information.id if run_information.id else None,
                run_entity_id=run_information.run_id,
                run_information_type=run_information.run_information_type.value,
                os=run_information.os.name,
                computer_name=run_information.computer_name,
                github_run_id=run_information.github_run_id,
                html_url=run_information.html_url,
                job_name=run_information.job_name,
                actor=run_information.actor,
                attempt=run_information.attempt,
                run_number=run_information.run_number,
                github_url=run_information.github_url,
                github_api_url=run_information.github_api_url,
            )
        raise ValueError(
            f"Unsupported run information type: {run_information.run_information_type}"
        )

    @staticmethod
    def _run_information_to_domain_object(entity: _BasicRunInformationMapping):
        if entity.run_information_type == RunBatchProvider.LOCAL_COMPUTER:
            entity = cast(_LocalComputerRunInformationMapping, entity)
            return LocalComputerRunInformation(
                id=entity.id,
                run_id=entity.run_entity_id,
                os=OS(entity.os),
                computer_name=entity.computer_name,
                local_username=entity.local_username,
            )
        elif entity.run_information_type == RunBatchProvider.GITHUB_ACTIONS:
            entity = cast(_GithubActionsRunInformationMapping, entity)
            return GithubActionsRunInformation(
                id=entity.id,
                run_id=entity.run_entity_id,
                os=OS(entity.os),
                computer_name=entity.computer_name,
                github_run_id=entity.github_run_id,
                html_url=entity.html_url,
                job_name=entity.job_name,
                actor=entity.actor,
                attempt=entity.attempt,
                run_number=entity.run_number,
                github_url=entity.github_url,
                github_api_url=entity.github_api_url,
            )
        raise ValueError(
            f"Unsupported run information type: {entity.run_information_type}"
        )
