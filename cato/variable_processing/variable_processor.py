from typing import Dict, Optional, List

from cato.domain.config import RunConfig
from cato.variable_processing.variable_predefinition import VariablePredefinition
from cato.vendor import lucidity


class VariableProcessor:
    def evaluate_variables(
        self,
        config: RunConfig,
        current_suite,
        test,
        predefinitions: Optional[List[VariablePredefinition]] = None,
    ) -> Dict[str, str]:
        default_variables = {
            "frame": "0001",
            "test_name": test.name,
            "suite_name": current_suite.name,
            "config_path": config.resource_path,
            "output_folder": config.output_folder,
            "test_resources": "{@config_path}/{@suite_name}/{@test_name}",
            "reference_image_no_extension": "{@test_resources}/reference",
            "reference_image_png": "{@reference_image_no_extension}.png",
            "reference_image_exr": "{@reference_image_no_extension}.exr",
            "image_output_folder": "{@output_folder}/result/{@suite_name}/{@test_name}",
            "image_output_no_extension": "{@image_output_folder}/{@test_name}",
            "image_output_png": "{@image_output_no_extension}.png",
            "image_output_exr": "{@image_output_no_extension}.exr",
        }
        if predefinitions:
            for predefinition in predefinitions:
                default_variables.update(predefinition.variables)
        default_variables.update(config.variables)
        default_variables.update(current_suite.variables)
        default_variables.update(test.variables)

        templates = {}
        for name, str in default_variables.items():
            template = lucidity.Template(name, str)
            template.template_resolver = templates
            templates[name] = template

        formatted = {}

        for name, template in templates.items():
            formatted[name] = template.format({})

        return formatted

    def format_command(self, command: str, variables: Dict[str, str]):
        templates = {}
        for name, str in variables.items():
            template = lucidity.Template(name, str)
            template.template_resolver = templates
            templates[name] = template
        command_template = lucidity.Template(command, command)
        command_template.template_resolver = templates
        return command_template.format(variables)
