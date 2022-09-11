from typing import Dict, Optional, List

import jinja2

from cato_common.domain.config import RunConfig
from cato_common.domain.test import Test
from cato_common.domain.test_suite import TestSuite
from cato.variable_processing.variable_predefinition import VariablePredefinition

import logging

logger = logging.getLogger(__name__)


class VariableSubstitutionRecursionDepthExceeded(Exception):
    def __init__(self, max_recursion_depth: int, template: str) -> None:
        super(VariableSubstitutionRecursionDepthExceeded, self).__init__(
            f"Max recursions ({max_recursion_depth}) exceeded for template '{template}'."
        )


class VariableProcessor:
    def evaluate_variables(
        self,
        config: RunConfig,
        current_suite: TestSuite,
        test: Test,
        predefinitions: Optional[List[VariablePredefinition]] = None,
    ) -> Dict[str, str]:
        default_variables = {
            "frame": "0001",
            "test_name": test.name,
            "suite_name": current_suite.name,
            "config_path": config.resource_path,
            "output_folder": config.output_folder,
            "suite_resources": "{{config_path}}/{{suite_name}}",
            "test_resources": "{{config_path}}/{{suite_name}}/{{test_name}}",
            "reference_image_no_extension": "{{test_resources}}/reference",
            "reference_image_png": "{{reference_image_no_extension}}.png",
            "reference_image_exr": "{{reference_image_no_extension}}.exr",
            "reference_image_jpg": "{{reference_image_no_extension}}.jpg",
            "reference_image_tif": "{{reference_image_no_extension}}.tif",
            "image_output_folder": "{{output_folder}}/result/{{suite_name}}/{{test_name}}",
            "image_output_no_extension": "{{image_output_folder}}/{{test_name}}",
            "image_output_png": "{{image_output_no_extension}}.png",
            "image_output_exr": "{{image_output_no_extension}}.exr",
            "image_output_jpg": "{{image_output_no_extension}}.jpg",
            "image_output_tif": "{{image_output_no_extension}}.tif",
        }
        if predefinitions:
            for predefinition in predefinitions:
                default_variables.update(predefinition.variables)
        default_variables.update(config.variables)
        default_variables.update(current_suite.variables)
        default_variables.update(test.variables)

        formatted = {}

        for name, template in default_variables.items():
            formatted[name] = self._render_recursive(template, default_variables)

        return formatted

    def format_command(self, command: str, variables: Dict[str, str]) -> str:
        return self._render_recursive(command, variables)

    def _render_recursive(self, template: str, variables: Dict[str, str]) -> str:
        previous = template
        max_recursion_depth = 50
        counter = 0
        while counter < max_recursion_depth:
            counter += 1
            curr = jinja2.Template(previous).render(**variables)
            if curr == previous:
                return curr
            previous = curr
        raise VariableSubstitutionRecursionDepthExceeded(max_recursion_depth, template)
