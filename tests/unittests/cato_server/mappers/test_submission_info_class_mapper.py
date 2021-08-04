import os

from cato_server.domain.submission_info import SubmissionInfo


def test_map_to_dict(config_fixture, object_mapper):
    submission_info = SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=42,
        resource_path="resource_path",
        executable="C:/Python27/python.exe",
    )

    the_dict = object_mapper.to_dict(submission_info)

    assert the_dict == {
        "id": 0,
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
                            "comparison_settings": {"method": "SSIM", "threshold": 0.8},
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


def test_map_from_dict(config_fixture, object_mapper):
    the_dict = {
        "id": 0,
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
                            "comparison_settings": {"method": "SSIM", "threshold": 0.8},
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

    submission_info = object_mapper.from_dict(the_dict, SubmissionInfo)
    config_fixture.CONFIG.resource_path = "this/is/a/random"
    config_fixture.CONFIG.output_folder = os.getcwd()

    assert submission_info == SubmissionInfo(
        id=0,
        config=config_fixture.CONFIG,
        run_id=42,
        resource_path="resource_path",
        executable="C:/Python27/python.exe",
    )
