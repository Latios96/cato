from cato.domain.Test import Test
from cato.reporter.Reporter import Reporter


class TestRunner:
    def __init__(self, reporter: Reporter):
        self._reporter = reporter

    def run_test(self, test: Test):
        self._reporter.report_start_test(test)
