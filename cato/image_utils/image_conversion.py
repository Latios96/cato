import logging

from oiio.OpenImageIO import ImageBuf, ImageBufAlgo

logger = logging.getLogger(__name__)


class ImageConversionError(Exception):
    pass


class ImageConverter:
    def convert(self, src, dst):
        logger.info("Converting image %s to %s using OpenImageIO..", src, dst)
        buf = ImageBuf(src)

        logger.info("Image has %s channels", buf.nchannels)
        if buf.nchannels > 4:
            logger.info("Image has more than 4 channels, stripping channels..")
            buf = ImageBufAlgo.channels(buf, (0, 1, 2, 3))
            logger.info("Stripped channels")

        logger.info("Writing image to %s", dst)
        ok = buf.write(dst)

        if not ok:
            raise ImageConversionError(
                "Error when converting image {} to {}: {}".format(
                    src, dst, buf.geterror()
                )
            )
