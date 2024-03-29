def test_should_existing_get_submission_info(client_with_session, submission_info):
    url = "/api/v1/submission_infos/{}".format(submission_info.id)

    rv = client_with_session.get(url)

    assert rv.status_code == 200
    assert rv.json() == {
        "config": {
            "projectName": "EXAMPLE_PROJECT",
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
                            "comparisonSettings": {"method": "SSIM", "threshold": 0.8},
                        }
                    ],
                    "variables": {"my_var": "from_suite"},
                }
            ],
            "variables": {"my_var": "from_config"},
        },
        "executable": "executable",
        "id": 1,
        "resourcePath": "resource_path",
        "runId": 1,
    }


def test_not_existing_should_return_404(client_with_session):
    url = "/api/v1/submission_infos/1"

    rv = client_with_session.get(url)

    assert rv.status_code == 404
