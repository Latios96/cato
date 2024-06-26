# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots["test_submit_command 1"] = [
    """[INFO]  Reporting execution start to server..
[INFO]  No project with name EXAMPLE_PROJECT exists, creating one..
[INFO]  Created project EXAMPLE_PROJECT with id 2.
[INFO]  Creating run..
[INFO]  Reporting execution of 1 suite and 1 test
[INFO]  You can find your run at http://127.0.0.1:12345/projects/2/runs/1
[INFO]  Submitting to scheduler..
[INFO]  Submitted 1 suite with 1 test to scheduler.
"""
]

snapshots["test_worker_run_command 1"] = [
    """[INFO]  Reporting execution start to server..
[INFO]  No project with name EXAMPLE_PROJECT exists, creating one..
[INFO]  Created project EXAMPLE_PROJECT with id 2.
[INFO]  Creating run..
[INFO]  Reporting execution of 1 suite and 1 test
[INFO]  You can find your run at http://127.0.0.1:12345/projects/2/runs/1
[INFO]  Submitting to scheduler..
[INFO]  Submitted 1 suite with 1 test to scheduler.
"""
]

snapshots["test_worker_run_command 2"] = [
    """[INFO]  Collecting machine info (once per day)..
[INFO]  Running PythonOutputVersion..
[INFO]  Command: <some command>
[INFO]  Copy <a> to <b>
[INFO]  Found image output at path <foo>
[INFO]  Found image output at path <bar>
[INFO]  Comparing images locally..
[INFO]  PythonOutputVersion succeeded in 0.12 seconds
[INFO]  Reporting test result of test PythonTestSuite/PythonOutputVersion..
[INFO]  Uploading output of test PythonTestSuite/PythonOutputVersion..
[INFO]  Done.
"""
]
