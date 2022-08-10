import os
import sys

import pytest

selenium_test = pytest.mark.flaky(reruns=1, condition=os.environ.get("CI") is not None)
testcontainers_test = pytest.mark.skipif(
    reason="Testcontainers don't work in CI on Windows for now",
    condition=sys.platform == "win32" and os.environ.get("CI") is not None,
)
