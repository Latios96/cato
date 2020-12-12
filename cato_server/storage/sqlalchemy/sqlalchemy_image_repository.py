import dataclasses

from sqlalchemy import Column, Integer, ForeignKey, String, JSON

from cato.domain.image import Image, ImageChannel
from cato_server.storage.abstract.abstract_image_repository import ImageRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class ImageMapping(Base):
    __tablename__ = "image_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    original_file_entity_id = Column(Integer, ForeignKey("file_entity.id"))
    channels = Column(JSON)


class SqlAlchemyImageRepository(
    AbstractSqlAlchemyRepository[Image, ImageMapping, int], ImageRepository
):
    def to_entity(self, domain_object: Image) -> ImageMapping:
        return ImageMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            original_file_entity_id=domain_object.original_file_id,
            channels=list(map(dataclasses.asdict, domain_object.channels)),
        )

    def to_domain_object(self, entity: ImageMapping) -> Image:
        return Image(
            id=entity.id,
            name=entity.name,
            original_file_id=entity.original_file_entity_id,
            channels=[ImageChannel(**x) for x in entity.channels],
        )

    def mapping_cls(self):
        return ImageMapping
