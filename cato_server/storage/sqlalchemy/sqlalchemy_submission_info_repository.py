from sqlalchemy import Column, Integer, JSON, ForeignKey, String

from cato.config.config_file_parser import JsonConfigParser
from cato.config.config_file_writer import ConfigFileWriter
from cato_server.domain.submission_info import SubmissionInfo
from cato_server.storage.abstract.submission_info_repository import (
    SubmissionInfoRepository,
)
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class _SubmissionInfoMapping(Base):
    __tablename__ = "submission_info_entity"

    id = Column(Integer, primary_key=True, autoincrement=True)
    config = Column(JSON, nullable=False)
    run_entity_id = Column(Integer, ForeignKey("run_entity.id"))
    resource_path = Column(String, nullable=False)
    executable = Column(String, nullable=False)


class SqlAlchemySubmissionInfoRepository(
    AbstractSqlAlchemyRepository, SubmissionInfoRepository
):
    def __init__(
        self,
        session_maker,
        json_config_parser: JsonConfigParser,
        config_file_writer: ConfigFileWriter,
    ):
        super(SqlAlchemySubmissionInfoRepository, self).__init__(session_maker)
        self._json_config_parser = json_config_parser
        self._config_file_writer = config_file_writer

    def to_entity(self, domain_object: SubmissionInfo) -> _SubmissionInfoMapping:
        return _SubmissionInfoMapping(
            id=domain_object.id if domain_object.id else None,
            config=self._config_file_writer.write_to_dict(domain_object.config),
            run_entity_id=domain_object.run_id,
            resource_path=domain_object.resource_path,
            executable=domain_object.executable,
        )

    def to_domain_object(self, entity: _SubmissionInfoMapping) -> SubmissionInfo:
        return SubmissionInfo(
            id=entity.id,
            config=self._json_config_parser.parse_dict(entity.config),
            run_id=entity.run_entity_id,
            resource_path=entity.resource_path,
            executable=entity.executable,
        )

    def mapping_cls(self):
        return _SubmissionInfoMapping
