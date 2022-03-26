# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_config_file_template 1"] = [
    """[INFO]  Wrote config file to SOME_RANDOM_DIR/cato.json
"""
]

snapshots[
    "test_list_tests_command_from_cwd 1"
] = """[INFO]  Found 1 tests in 1 suites:
[INFO]  
[INFO]  My_first_test_Suite/My_first_test
"""

snapshots[
    "test_list_tests_command_from_path 1"
] = """[INFO]  Found 1 tests in 1 suites:
[INFO]  
[INFO]  My_first_test_Suite/My_first_test
"""

snapshots["test_submit_command 1"] = [
    """[INFO]  Reporting execution start to server..
[INFO]  No project with name EXAMPLE_PROJECT exists, creating one..
[INFO]  Created project Project(id=2, name='EXAMPLE_PROJECT')
[INFO]  Creating run..
[INFO]  Reporting execution of 1 suite and 1 test
[INFO]  You can find your run at http://127.0.0.1:12345/projects/2/runs/1
[INFO]  Submitting to scheduler..
[INFO]  Submitted 1 suite with 1 test to scheduler.
"""
]

snapshots["test_update_missing_reference_images_should_have_no_effect 1"] = ""

snapshots["test_update_reference_should_have_no_effect 1"] = ""

snapshots["test_worker_run_command 1"] = [
    """[INFO]  Reporting execution start to server..
[INFO]  No project with name EXAMPLE_PROJECT exists, creating one..
[INFO]  Created project Project(id=2, name='EXAMPLE_PROJECT')
[INFO]  Creating run..
[INFO]  Reporting execution of 1 suite and 1 test
[INFO]  You can find your run at http://127.0.0.1:12345/projects/2/runs/1
[INFO]  Submitting to scheduler..
[INFO]  Submitted 1 suite with 1 test to scheduler.
"""
]

snapshots["test_worker_run_command 2"] = [
    """[INFO]  Collecting machine info..
[INFO]  Running PythonOutputVersion..
[INFO]  Command: <some command>
[INFO]  Copy <a> to <b>
[INFO]  Found image output at path <foo>
[INFO]  Found image output at path <bar>
[INFO]  Comparing images on the server..
[INFO]  PythonOutputVersion succeeded in 0.12 seconds
[INFO]  Reporting test result of test PythonTestSuite/PythonOutputVersion..
[INFO]  Uploading output of test PythonTestSuite/PythonOutputVersion..
[INFO]  Done.
"""
]
