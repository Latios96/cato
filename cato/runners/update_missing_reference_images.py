import os
import shutil
from typing import Callable

from cato import logger
from cato.domain.config import RunConfig
from cato.domain.test_suite import iterate_suites_and_tests
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.variable_processing.variable_processor import VariableProcessor


class UpdateMissingReferenceImages:
    def __init__(
        self,
        output_folder: OutputFolder,
        copy_file: Callable[[str, str], None] = shutil.copy,
    ):
        self._output_folder = output_folder
        self._copy_file = copy_file

    def update(self, config: RunConfig) -> None:
        for suite, test in iterate_suites_and_tests(config.suites):
            variable_processor = VariableProcessor()
            variables = variable_processor.evaluate_variables(config, suite, test)

            image_outputs = [
                variables["image_output_exr"],
                variables["image_output_png"],
            ]
            image_output = variables.get("image_output")
            if image_output:
                image_outputs.append(image_output)
            image_output = self._output_folder.any_existing(image_outputs)

            reference_images = [
                variables["reference_image_exr"],
                variables["reference_image_png"],
            ]
            reference_image = variables.get("reference_image")
            if reference_image:
                reference_images.append(reference_image)
            reference_image = self._output_folder.any_existing(reference_images)

            if image_output and not reference_image:
                target_path = (
                    variables["reference_image_no_extension"]
                    + os.path.splitext(image_output)[1]
                )
                logger.info(f"Copy {image_output} to {target_path}..")
                self._copy_file(image_output, target_path)
