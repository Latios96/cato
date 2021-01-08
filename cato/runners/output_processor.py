import logging

from cato.reporter.reporter import Reporter

logger = logging.getLogger(__name__)


class OutputProcessor:
    def __init__(self, reporter: Reporter):
        self._reporter = reporter

    def process(self, line: str) -> None:
        self._reporter.report_command_output(line.strip())
