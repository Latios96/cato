from dataclasses import dataclass

from cato_common.domain.image import Image


@dataclass
class StoreImageResult:
    image: Image
