import os
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Optional

from cato_common.domain.comparison_result import ComparisonResult
from cato_common.domain.comparison_settings import ComparisonSettings
from cato_common.domain.result_status import ResultStatus

import logging

logger = logging.getLogger(__name__)


class FlipImageComparator:
    def compare(
        self,
        reference: str,
        output: str,
        comparison_settings: ComparisonSettings,
        workdir: str,
    ) -> ComparisonResult:
        reference_and_output_are_the_same = os.path.abspath(
            reference
        ) == os.path.abspath(output)
        if reference_and_output_are_the_same:
            raise ValueError(
                f"Images to compare need to be different, pointing to same path: {os.path.abspath(reference)}"
            )

        same_format_error = self._verify_images_have_same_format(reference, output)
        if same_format_error:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=same_format_error,
                diff_image=None,
                error=1,
            )

        # check resolution
        # compare images

        flip_executable = Path(__file__).parent / "nvidia_flip" / "flip.py"
        diff_image_basename = f"diff_image_{uuid.uuid4()}"
        args = [
            sys.executable,
            str(flip_executable),
            "-r",
            reference,
            "-t",
            output,
            "--directory",
            workdir,
            "--basename",
            diff_image_basename,
            "--textfile",
            "--start_exposure",
            "0",
            "--stop_exposure",
            "1",
        ]

        status, process_output = subprocess.getstatusoutput(" ".join(args))
        if status != 0:
            if (
                "Invalid image format" in process_output
                or "cannot identify image file" in process_output
            ):
                raise ValueError(
                    f"Could not read image from {output}, unsupported file format!"
                )
            if "Images have different resolutions" in process_output:
                return ComparisonResult(
                    status=ResultStatus.FAILED,
                    message=process_output.split("\n")[-1].replace(
                        "AssertionError: ", ""
                    ),
                    diff_image=None,
                    error=0,
                )
            raise RuntimeError(process_output)

        diff_image = os.path.join(workdir, diff_image_basename + ".png")
        result_text_file = os.path.join(workdir, diff_image_basename + ".txt")

        if not os.path.exists(result_text_file):
            raise RuntimeError("result txt does not exist")
        with open(result_text_file) as f:
            mean_line = f.readline()
        mean_error = float(mean_line.split(" ")[1])

        if mean_error > comparison_settings.threshold:
            return ComparisonResult(
                status=ResultStatus.FAILED,
                message=f"Images are not equal! FLIP mean error was {mean_error:.3f}, max threshold is {comparison_settings.threshold:.3f}",
                diff_image=diff_image,
                error=mean_error,
            )

        return ComparisonResult(
            status=ResultStatus.SUCCESS,
            message=None,
            diff_image=diff_image,
            error=mean_error,
        )

    def _verify_images_have_same_format(
        self, reference: str, output: str
    ) -> Optional[str]:
        reference_image_extension = os.path.splitext(reference)[1]
        output_image_extension = os.path.splitext(output)[1]

        if reference_image_extension != output_image_extension:
            return f"FLIP does not support comparison of reference {reference_image_extension} to output {output_image_extension}, image need to have same format."
