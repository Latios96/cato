from typing import Optional

from sqlalchemy import Column, Integer, Text, ForeignKey

from cato_common.domain.output import Output
from cato_server.storage.abstract.output_repository import OutputRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class OutputMapping(Base):
    __tablename__ = "output_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_result_entity_id = Column(
        Integer, ForeignKey("test_result_entity.id"), unique=True
    )
    text = Column(Text, nullable=False)


class SqlAlchemyOutputRepository(
    AbstractSqlAlchemyRepository[Output, OutputMapping, int], OutputRepository
):
    def to_entity(self, domain_object: Output) -> OutputMapping:
        return OutputMapping(
            id=domain_object.id if domain_object.id else None,
            test_result_entity_id=domain_object.test_result_id,
            text=domain_object.text,
        )

    def to_domain_object(self, entity: OutputMapping) -> Output:
        return Output(
            id=entity.id, test_result_id=entity.test_result_entity_id, text=entity.text
        )

    def mapping_cls(self):
        return OutputMapping

    def find_by_test_result_id(self, id) -> Optional[Output]:
        with self._session_maker() as session:
            query = session.query(self.mapping_cls()).filter(
                self.mapping_cls().test_result_entity_id == id
            )

            return self._map_one_to_domain_object(query.first())
