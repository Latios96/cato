import os
import shutil

from cato import logger
from cato.domain.config import Config
from cato.domain.test_suite import iterate_suites_and_tests
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.runners.variable_processor import VariableProcessor


class UpdateMissingReferenceImages:
    def __init__(self, output_folder: OutputFolder):
        self._output_folder = output_folder

    def update(self, config: Config):
        for suite, test in iterate_suites_and_tests(config.test_suites):
            variable_processor = VariableProcessor()
            variables = variable_processor.evaluate_variables(
                config, suite, test
            )

            image_outputs = [
                variables["image_output_exr"],
                variables["image_output_png"],
            ]
            if variables.get("image_output"):
                image_outputs.append(variables.get("image_output"))
            image_output = self._output_folder.any_existing(image_outputs)

            reference_images = [
                variables["reference_image_exr"],
                variables["reference_image_png"],
            ]
            if variables.get("reference_image"):
                reference_images.append(variables.get("reference_image"))
            reference_image = self._output_folder.any_existing(reference_images)

            if image_output and not reference_image:
                target_path = (
                    variables["reference_image_no_extension"]
                    + os.path.splitext(image_output)[1]
                )
                logger.info(f"Copy {image_output} to {target_path}..")
                shutil.copy(image_output, target_path)
