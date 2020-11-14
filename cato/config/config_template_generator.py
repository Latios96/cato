import json
from typing import IO

TEMPLATE = {
    "suites": [
        {
            "name": "My First Test Suite",
            "tests": [
                {"name": "My First Test", "command": "python --version"},
                {
                    "name": "use {test_resources} to get test resource folder",
                    "command": "python --version {test_resources}",
                },
                {
                    "name": "use {image_output_png} to get path where to put image",
                    "command": "python --version {image_output_png}",
                },
            ],
        }
    ]
}


class ConfigTemplateGenerator:
    def write(self, stream: IO):
        stream.write(json.dumps(TEMPLATE, indent=2))
