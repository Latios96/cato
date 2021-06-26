import os
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List

import cv2
import numpy as np
from PIL import Image, ImageChops, ImageEnhance
from skimage import metrics

from cato_server import server_logging

from cato_server.images.image_splitter import ImageSplitter
from cato_server.images.oiio_binaries_discovery import OiioBinariesDiscovery


@dataclass
class TestCase:
    name: str
    reference_image: Path
    output_image: Path


def collect_test_cases() -> List[TestCase]:
    cases = []
    images_folder = Path(r'M:\testImages\difference test images\different_vray_version')
    for case_folder in images_folder.iterdir():
        case_name = case_folder.name
        output_path = case_folder / (case_name + ".exr")
        reference_path = case_folder / "reference.exr"
        cases.append(TestCase(name=case_name, reference_image=reference_path, output_image=output_path))
    return cases


def pillow(test_case: TestCase, work_dir):
    case_work_dir = work_dir / test_case.name / "Pillow"
    os.makedirs(case_work_dir)

    image_splitter.split_image_into_channels(str(test_case.output_image), str(case_work_dir))
    image_splitter.split_image_into_channels(str(test_case.reference_image), str(case_work_dir))

    output_image = Image.open(case_work_dir / (test_case.name + ".rgb.png"))
    reference_image = Image.open(case_work_dir / ("reference.rgb.png"))
    difference = ImageChops.difference(output_image, reference_image)
    enhancer = ImageEnhance.Brightness(difference)
    output = enhancer.enhance(50)
    output.save(case_work_dir / (test_case.name + ".difference.png"))


def opencv(test_case: TestCase, work_dir):
    case_work_dir = work_dir / test_case.name / "OpenCV"
    os.makedirs(case_work_dir)

    image_splitter.split_image_into_channels(str(test_case.output_image), str(case_work_dir))
    image_splitter.split_image_into_channels(str(test_case.reference_image), str(case_work_dir))

    output_image = cv2.imread(str(case_work_dir / (test_case.name + ".rgb.png")), )
    reference_image = cv2.imread(str(case_work_dir / ("reference.rgb.png")))

    (score, diff) = metrics.structural_similarity(reference_image, output_image, full=True, multichannel=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    diff_gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    diff_gray = ~diff_gray

    black_channel = np.ones(diff_gray.shape, dtype=diff_gray.dtype)
    weighted_green = cv2.merge((black_channel, diff_gray, black_channel))


    filled_after = cv2.addWeighted(output_image, 1,weighted_green, 1,0)

    # implement using https://stackoverflow.com/questions/56183201/detect-and-visualize-differences-between-two-images-with-opencv-python

    cv2.imwrite(str(case_work_dir / (test_case.name + ".difference.png")), filled_after)
    cv2.imwrite(str(case_work_dir / (test_case.name + ".diff_gray.png")), diff_gray)
# todo implement threshold

    #cv2.imshow("diff_gray", diff_gray)
    #cv2.imshow("weighted_green", weighted_green)
    #cv2.imshow("filled_after", filled_after)
    #cv2.waitKey(0)



if __name__ == '__main__':
    image_splitter = ImageSplitter(OiioBinariesDiscovery())

    test_cases = collect_test_cases()

    work_dir = Path(__file__).parent / 'workdir'
    if work_dir.exists():
        shutil.rmtree(work_dir)
    work_dir.mkdir()

    # pillow(test_cases[0], work_dir)
    # opencv(test_cases[0], work_dir)
    first = True
    for test_case in test_cases:
        #if first:
        opencv(test_case, work_dir)
        first = False
