import cv2
from PIL import Image, ImageChops
from skimage import metrics


def images_are_equal(image1, image2):
    image_one = Image.open(image1)
    image_two = Image.open(image2)
    diff = ImageChops.difference(image_one, image_two)
    if diff.getbbox():
        return False
    return True


def _normalize_image(image):
    if image.dtype == "uint8":
        image = image.astype("float32")
        image /= 255.0
        return image
    elif image.dtype == "uint16":
        image = image.astype("float32")
        image /= 65535
        return image
    elif image.dtype == "float32":
        return image


def images_are_visually_equal(image1, image2, threshold):
    image_one = _normalize_image(
        cv2.imread(image1, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    )
    image_two = _normalize_image(
        cv2.imread(image2, cv2.IMREAD_COLOR | cv2.IMREAD_ANYDEPTH)
    )

    (score, diff) = metrics.structural_similarity(
        image_one,
        image_two,
        full=True,
        channel_axis=-1,
        data_range=image_two.max() - image_two.min(),
    )
    print(score)
    return score > threshold
