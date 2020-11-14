import os

from cato.domain.test import Test
from cato.domain.test_suite import TestSuite


class OutputFolderCreator:
    def create_folder(self, base: str, test_suite: TestSuite, test: Test):
        path = os.path.join(base, "result", test_suite.name, test.name)

        if not os.path.exists(path):
            os.makedirs(path)
