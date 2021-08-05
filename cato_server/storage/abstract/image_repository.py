from cato_common.domain.image import Image
from cato_server.storage.abstract.abstract_repository import AbstractRepository


class ImageRepository(AbstractRepository[Image, int]):
    pass
