import os

import pytest

selenium_test = pytest.mark.flaky(reruns=1, condition=os.environ.get("CI") is not None)
