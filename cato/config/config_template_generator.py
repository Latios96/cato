import json
from typing import IO

TEMPLATE = {
    "project_name": "Example",
    "suites": [
        {
            "name": "My_first_test_Suite",
            "tests": [
                {"name": "My_first_test", "command": "python --version"},
                {
                    "name": "use {@test_resources} to get test resource folder",
                    "command": "python --version {@test_resources}",
                },
                {
                    "name": "use {@image_output_png} to get path where to put image",
                    "command": "python --version {@image_output_png}",
                },
                {
                    "name": "use own variables in command",
                    "variables": {"frame": "7"},
                    "command": "python --version {@frame}",
                },
                {
                    "name": "define own image output if renderer does not support settings full path",
                    "variables": {
                        "image_output": "{@image_output_folder}/my_render.png"
                    },
                    "command": "python --version {@image_output}",
                },
            ],
        }
    ]
}


class ConfigTemplateGenerator:
    def write(self, stream: IO):
        stream.write(json.dumps(TEMPLATE, indent=2))
