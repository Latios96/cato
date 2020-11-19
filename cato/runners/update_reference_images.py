import os
import shutil

from cato import logger
from cato.domain.config import Config
from cato.domain.test_identifier import TestIdentifier
from cato.domain.test_suite import iterate_suites_and_tests, filter_by_test_identifier
from cato.file_system_abstractions.output_folder import OutputFolder
from cato.variable_processing.variable_processor import VariableProcessor


class UpdateReferenceImages:
    def __init__(self, output_folder: OutputFolder):
        self._output_folder = output_folder

    def update(self, config: Config, test_identifier: TestIdentifier):
        filtered = filter_by_test_identifier(config.test_suites, test_identifier)
        for suite, test in iterate_suites_and_tests(filtered):
            variable_processor = VariableProcessor()
            variables = variable_processor.evaluate_variables(config, suite, test)

            image_outputs = [
                variables["image_output_exr"],
                variables["image_output_png"],
            ]
            if variables.get("image_output"):
                image_outputs.append(variables.get("image_output"))
            image_output = self._output_folder.any_existing(image_outputs)

            if image_output:
                target_path = (
                    variables["reference_image_no_extension"]
                    + os.path.splitext(image_output)[1]
                )
                logger.info(f"Copy {image_output} to {target_path}..")
                shutil.copy(image_output, target_path)
