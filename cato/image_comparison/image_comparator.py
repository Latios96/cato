import os
from dataclasses import dataclass

from oiio.OpenImageIO import ImageBuf, ImageBufAlgo


@dataclass
class CompareResults:
    meanerror: float
    rms_error: float
    PSNR: float
    maxerror: float
    maxx: int
    maxy: int
    maxz: int
    maxc: int
    nwarn: int
    nfail: int
    error: bool


class ImageComparator:

    def compare(self, left: str, right: str):
        assert os.path.exists(left)
        assert os.path.exists(right)

        left_input = ImageBuf(left)
        right_input = ImageBuf(right)
        result = ImageBufAlgo.compare(left_input, right_input, 0.5, 0)

        return CompareResults(
            meanerror=result.meanerror,
            rms_error=result.rms_error,
            PSNR=result.PSNR,
            maxerror=result.maxerror,
            maxx=result.maxx,
            maxy=result.maxy,
            maxz=result.maxz,
            maxc=result.maxc,
            nwarn=result.nwarn,
            nfail=result.nfail,
            error=result.error
        )
