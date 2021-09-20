from typing import Optional, List, cast

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float
from sqlalchemy.orm import with_polymorphic

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato_server.domain.test_edit import (
    AbstractTestEdit,
    EditTypes,
    ComparisonSettingsEditValue,
    ComparisonSettingsEdit,
    ReferenceImageEdit,
)
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

    __mapper_args__ = {"polymorphic_identity": "test_edit", "polymorphic_on": edit_type}


class _ComparisonSettingsEditMapping(_TestEditMapping):
    __tablename__ = "comparison_settings_edit_entity"

    id = Column(Integer, ForeignKey("test_edit_entity.id"), primary_key=True)
    old_comparison_method = Column(String, nullable=False)
    new_comparison_method = Column(String, nullable=False)
    old_threshold = Column(Float, nullable=False)
    new_threshold = Column(Float, nullable=False)

    __mapper_args__ = {
        "polymorphic_identity": EditTypes.COMPARISON_SETTINGS.value,
    }


class _ReferenceImageEditMapping(_TestEditMapping):
    __tablename__ = "reference_image_edit_entity"

    id = Column(Integer, ForeignKey("test_edit_entity.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": EditTypes.REFERENCE_IMAGE.value,
    }


class SqlAlchemyTestEditRepository(AbstractSqlAlchemyRepository, TestEditRepository):
    def to_entity(self, domain_object: AbstractTestEdit) -> _TestEditMapping:
        if domain_object.edit_type == EditTypes.COMPARISON_SETTINGS:
            domain_object = cast(ComparisonSettingsEdit, domain_object)
            return _ComparisonSettingsEditMapping(
                id=domain_object.id if domain_object.id else None,
                test_id=domain_object.test_id,
                edit_type=domain_object.edit_type.value,
                created_at=domain_object.created_at,
                new_comparison_method=domain_object.new_value.comparison_settings.method.value,
                new_threshold=domain_object.new_value.comparison_settings.threshold,
                old_comparison_method=domain_object.old_value.comparison_settings.method.value,
                old_threshold=domain_object.old_value.comparison_settings.threshold,
            )
        elif domain_object.edit_type == EditTypes.REFERENCE_IMAGE:
            domain_object = cast(ReferenceImageEdit, domain_object)
            return _ReferenceImageEditMapping(
                id=domain_object.id if domain_object.id else None,
                test_id=domain_object.test_id,
                edit_type=domain_object.edit_type.value,
                created_at=domain_object.created_at,
            )
        raise ValueError(f"Unsupported edit type: {domain_object.edit_type}")

    def to_domain_object(self, entity: _TestEditMapping) -> AbstractTestEdit:
        if entity.edit_type == EditTypes.COMPARISON_SETTINGS.value:
            entity = cast(_ComparisonSettingsEditMapping, entity)
            return ComparisonSettingsEdit(
                id=entity.id,
                test_id=entity.test_id,
                created_at=entity.created_at,
                new_value=ComparisonSettingsEditValue(
                    comparison_settings=ComparisonSettings(
                        method=ComparisonMethod(entity.new_comparison_method),
                        threshold=entity.new_threshold,
                    )
                ),
                old_value=ComparisonSettingsEditValue(
                    comparison_settings=ComparisonSettings(
                        method=ComparisonMethod(entity.old_comparison_method),
                        threshold=entity.old_threshold,
                    )
                ),
            )
        elif entity.edit_type == EditTypes.REFERENCE_IMAGE.value:
            entity = cast(_ReferenceImageEditMapping, entity)
            return ReferenceImageEdit(
                id=entity.id,
                test_id=entity.test_id,
                created_at=entity.created_at,
            )
        raise ValueError(f"Unsupported edit type: {entity.edit_type}")

    def mapping_cls(self):
        return _TestEditMapping

    def find_by_test_id(
        self, test_id: int, edit_type: Optional[EditTypes] = None
    ) -> List[AbstractTestEdit]:
        session = self._session_maker()

        query = session.query(
            with_polymorphic(_TestEditMapping, [_ComparisonSettingsEditMapping])
        ).filter(self.mapping_cls().test_id == test_id)

        if edit_type is not None:
            query = query.filter(self.mapping_cls().edit_type == edit_type.value)

        entities = query.order_by(self.mapping_cls().created_at.desc()).all()

        session.close()
        return list(map(self.to_domain_object, entities))

    def find_by_run_id(self, run_id: int) -> List[AbstractTestEdit]:
        session = self._session_maker()

        entities = (
            session.query(
                with_polymorphic(_TestEditMapping, [_ComparisonSettingsEditMapping])
            )
            .join(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .order_by(self.mapping_cls().created_at.desc())
            .all()
        )

        session.close()
        return list(map(self.to_domain_object, entities))
