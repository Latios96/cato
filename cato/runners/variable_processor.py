from typing import Dict

from cato.vendor import lucidity


class VariableProcessor:
    def evaluate_variables(
        self, config, current_suite, test, variables: Dict[str, str]
    ) -> Dict[str, str]:
        default_variables = {
            "test_name": test.name,
            "suite_name": current_suite.name,
            "config_path": config.path,
            "test_resources": "{@config_path}/{@suite_name}/{@test_name}",
            "image_output_folder": "{@test_resources}/{@suite_name}/{@test_name}",
            "image_output_no_extension": "{@image_output_folder}/{@test_name}",
            "image_output_png": "{@image_output_no_extension}.png",
        }
        default_variables.update(variables)

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
