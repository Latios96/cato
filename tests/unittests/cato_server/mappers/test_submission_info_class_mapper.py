import os

from cato_server.mappers.internal.submission_info_class_mapper import (
    SubmissionInfoClassMapper,
)
from cato_server.schedulers.submission_info import SubmissionInfo


def test_map_to_dict(config_fixture):
    submission_info = SubmissionInfo(
        config=config_fixture.CONFIG,
        run_id=42,
        resource_path="resource_path",
        executable="C:/Python27/python.exe",
    )

    the_dict = SubmissionInfoClassMapper().map_to_dict(submission_info)

    assert the_dict == {
        "config": {
            "project_name": "EXAMPLE_PROJECT",
            "suites": [
                {
                    "name": "My_first_test_Suite",
                    "tests": [
                        {
                            "command": "mayabatch -s "
                            "{config_file_folder}/{test_name.json} "
                            "-o "
                            "{image_output}/{test_name.png}",
                            "name": "My_first_test",
                            "variables": {"frame": "7"},
                        }
                    ],
                    "variables": {"my_var": "from_suite"},
                }
            ],
            "variables": {"my_var": "from_config"},
        },
        "executable": "C:/Python27/python.exe",
        "resource_path": "resource_path",
        "run_id": 42,
    }


def test_map_from_dict(config_fixture):
    the_dict = {
        "config": {
            "project_name": "EXAMPLE_PROJECT",
            "suites": [
                {
                    "name": "My_first_test_Suite",
                    "tests": [
                        {
                            "command": "mayabatch -s "
                            "{config_file_folder}/{test_name.json} "
                            "-o "
                            "{image_output}/{test_name.png}",
                            "name": "My_first_test",
                            "variables": {"frame": "7"},
                        }
                    ],
                    "variables": {"my_var": "from_suite"},
                }
            ],
            "variables": {"my_var": "from_config"},
        },
        "executable": "C:/Python27/python.exe",
        "resource_path": "resource_path",
        "run_id": 42,
    }

    submission_info = SubmissionInfoClassMapper().map_from_dict(the_dict)
    config_fixture.CONFIG.resource_path = "this/is/a/random"
    config_fixture.CONFIG.output_folder = os.getcwd()

    assert submission_info == SubmissionInfo(
        config=config_fixture.CONFIG,
        run_id=42,
        resource_path="resource_path",
        executable="C:/Python27/python.exe",
    )
