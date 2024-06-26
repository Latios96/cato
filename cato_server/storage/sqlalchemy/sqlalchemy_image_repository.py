from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship, joinedload

from cato_common.domain.image import Image, ImageChannel, ImageTranscodingState
from cato_server.storage.abstract.image_repository import ImageRepository
from cato_server.storage.sqlalchemy.abstract_sqlalchemy_repository import (
    AbstractSqlAlchemyRepository,
    Base,
)


class ImageChannelMapping(Base):
    __tablename__ = "image_channel_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_entity_id = Column(Integer, ForeignKey("image_entity.id"))
    name = Column(String, nullable=False)
    file_entity_id = Column(Integer, ForeignKey("file_entity.id"))


class ImageMapping(Base):
    __tablename__ = "image_entity"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    original_file_entity_id = Column(Integer, ForeignKey("file_entity.id"))
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    channels = relationship(ImageChannelMapping)
    transcoding_state = Column(String, nullable=False)


class SqlAlchemyImageRepository(
    AbstractSqlAlchemyRepository[Image, ImageMapping, int], ImageRepository
):
    def to_entity(self, domain_object: Image) -> ImageMapping:
        return ImageMapping(
            id=domain_object.id if domain_object.id else None,
            name=domain_object.name,
            original_file_entity_id=domain_object.original_file_id,
            width=domain_object.width,
            height=domain_object.height,
            channels=list(map(self._map_channel_to_entity, domain_object.channels)),
            transcoding_state=domain_object.transcoding_state.name,
        )

    def _map_channel_to_entity(
        self, domain_object: ImageChannel
    ) -> ImageChannelMapping:
        return ImageChannelMapping(
            id=domain_object.id if domain_object.id else None,
            image_entity_id=domain_object.image_id if domain_object.image_id else None,
            name=domain_object.name,
            file_entity_id=domain_object.file_id,
        )

    def to_domain_object(self, entity: ImageMapping) -> Image:
        return Image(
            id=entity.id,
            name=entity.name,
            original_file_id=entity.original_file_entity_id,
            channels=list(map(self._map_channel_to_domain_object, entity.channels)),
            width=entity.width,
            height=entity.height,
            transcoding_state=ImageTranscodingState(entity.transcoding_state),
        )

    def _map_channel_to_domain_object(
        self, entity: ImageChannelMapping
    ) -> ImageChannel:
        return ImageChannel(
            id=entity.id,
            image_id=entity.image_entity_id,
            name=entity.name,
            file_id=entity.file_entity_id,
        )

    def mapping_cls(self):
        return ImageMapping

    def default_query_options(self):
        return [joinedload(ImageMapping.channels)]
