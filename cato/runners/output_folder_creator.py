import logging
import os
from typing import Optional

from cato.domain.test import Test
from cato.domain.test_suite import TestSuite

logger = logging.getLogger(__name__)


class OutputFolder:
    def create_folder(self, base: str, test_suite: TestSuite, test: Test):
        path = os.path.join(base, "result", test_suite.name, test.name)

        if not os.path.exists(path):
            os.makedirs(path)

    def image_output_exists(self, image_output):
        return os.path.exists(image_output)

    def reference_image_exists(self, reference_image):
        return os.path.exists(reference_image)

    def any_existing(self, paths) -> Optional[str]:
        for path in paths:
            if os.path.exists(path):
                return path
        return None
