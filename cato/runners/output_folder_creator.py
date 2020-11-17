import os

from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class OutputFolder:
    def create_folder(self, base: str, test_suite: TestSuite, test: Test):
        path = os.path.join(base, "result", test_suite.name, test.name)

        if not os.path.exists(path):
            os.makedirs(path)

    def image_output_exists(self, image_output):
        return os.path.exists(image_output)

    def reference_image_exists(self, reference_image):
        return os.path.exists(image_output)
