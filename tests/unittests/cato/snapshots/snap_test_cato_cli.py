# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots[
    "test_config_file_template 1"
] = """[INFO]  Wrote config file to SOME_RANDOM_DIR/cato.json
"""

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

snapshots["test_update_missing_reference_images_should_have_no_effect 1"] = ""

snapshots["test_update_reference_should_have_no_effect 1"] = ""
