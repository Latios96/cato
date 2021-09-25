from typing import Optional, List, cast

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, func
from sqlalchemy.orm import with_polymorphic

from cato.domain.comparison_method import ComparisonMethod
from cato.domain.comparison_settings import ComparisonSettings
from cato.domain.test_status import TestStatus
from cato_server.domain.test_edit import (
    AbstractTestEdit,
    EditTypes,
    ComparisonSettingsEditValue,
    ComparisonSettingsEdit,
    ReferenceImageEdit,
    ReferenceImageEditValue,
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
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)
    old_message = Column(String, nullable=True)
    new_message = Column(String, nullable=True)
    old_diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    new_diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    old_error_value = Column(Float, nullable=True)
    new_error_value = Column(Float, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": EditTypes.COMPARISON_SETTINGS.value,
    }


class _ReferenceImageEditMapping(_TestEditMapping):
    __tablename__ = "reference_image_edit_entity"

    id = Column(Integer, ForeignKey("test_edit_entity.id"), primary_key=True)

    old_reference_image_id = Column(
        Integer, ForeignKey("image_entity.id"), nullable=True
    )
    new_reference_image_id = Column(
        Integer, ForeignKey("image_entity.id"), nullable=True
    )
    old_diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    new_diff_image_id = Column(Integer, ForeignKey("image_entity.id"), nullable=True)
    old_status = Column(String, nullable=True)
    new_status = Column(String, nullable=True)
    old_message = Column(String, nullable=True)
    new_message = Column(String, nullable=True)
    old_error_value = Column(Float, nullable=True)
    new_error_value = Column(Float, nullable=True)

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
                old_status=domain_object.old_value.status.value,
                old_message=domain_object.old_value.message,
                old_diff_image_id=domain_object.old_value.diff_image_id,
                new_status=domain_object.new_value.status.value,
                new_message=domain_object.new_value.message,
                new_diff_image_id=domain_object.new_value.diff_image_id,
                new_error_value=domain_object.new_value.error_value,
                old_error_value=domain_object.old_value.error_value,
            )
        elif domain_object.edit_type == EditTypes.REFERENCE_IMAGE:
            domain_object = cast(ReferenceImageEdit, domain_object)
            return _ReferenceImageEditMapping(
                id=domain_object.id if domain_object.id else None,
                test_id=domain_object.test_id,
                edit_type=domain_object.edit_type.value,
                created_at=domain_object.created_at,
                old_reference_image_id=domain_object.old_value.reference_image_id,
                new_reference_image_id=domain_object.new_value.reference_image_id,
                old_diff_image_id=domain_object.old_value.diff_image_id,
                new_diff_image_id=domain_object.new_value.diff_image_id,
                old_status=domain_object.old_value.status.value,
                new_status=domain_object.new_value.status.value,
                old_message=domain_object.old_value.message,
                new_message=domain_object.new_value.message,
                new_error_value=domain_object.new_value.error_value,
                old_error_value=domain_object.old_value.error_value,
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
                    ),
                    status=TestStatus(entity.new_status),
                    message=entity.new_message,
                    diff_image_id=entity.new_diff_image_id,
                    error_value=entity.new_error_value,
                ),
                old_value=ComparisonSettingsEditValue(
                    comparison_settings=ComparisonSettings(
                        method=ComparisonMethod(entity.old_comparison_method),
                        threshold=entity.old_threshold,
                    ),
                    status=TestStatus(entity.old_status),
                    message=entity.old_message,
                    diff_image_id=entity.old_diff_image_id,
                    error_value=entity.old_error_value,
                ),
            )
        elif entity.edit_type == EditTypes.REFERENCE_IMAGE.value:
            entity = cast(_ReferenceImageEditMapping, entity)
            return ReferenceImageEdit(
                id=entity.id,
                test_id=entity.test_id,
                created_at=entity.created_at,
                old_value=ReferenceImageEditValue(
                    status=TestStatus(entity.old_status),
                    message=entity.old_message,
                    reference_image_id=entity.old_reference_image_id,
                    diff_image_id=entity.old_diff_image_id,
                    error_value=entity.old_error_value,
                ),
                new_value=ReferenceImageEditValue(
                    status=TestStatus(entity.new_status),
                    message=entity.new_message,
                    reference_image_id=entity.new_reference_image_id,
                    diff_image_id=entity.new_diff_image_id,
                    error_value=entity.new_error_value,
                ),
            )
        raise ValueError(f"Unsupported edit type: {entity.edit_type}")

    def mapping_cls(self):
        return _TestEditMapping

    def find_by_test_id(
        self, test_id: int, edit_type: Optional[EditTypes] = None
    ) -> List[AbstractTestEdit]:
        session = self._session_maker()

        query = session.query(
            with_polymorphic(
                _TestEditMapping,
                [_ComparisonSettingsEditMapping, _ReferenceImageEditMapping],
            )
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
                with_polymorphic(
                    _TestEditMapping,
                    [_ComparisonSettingsEditMapping, _ReferenceImageEditMapping],
                )
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

    def find_edits_to_sync_by_run_id(self, run_id: int) -> List[AbstractTestEdit]:
        session = self._session_maker()

        entities = (
            session.query(
                with_polymorphic(
                    _TestEditMapping,
                    [_ComparisonSettingsEditMapping, _ReferenceImageEditMapping],
                ),
                func.max(_TestEditMapping.id),
                _TestResultMapping.test_identifier,
            )
            .join(_TestResultMapping)
            .join(_SuiteResultMapping)
            .join(_RunMapping)
            .filter(_RunMapping.id == run_id)
            .group_by(_TestEditMapping.edit_type)
            .group_by(_TestEditMapping.test_id)
            .all()
        )

        session.close()
        return list(map(lambda x: self.to_domain_object(x[0]), entities))
