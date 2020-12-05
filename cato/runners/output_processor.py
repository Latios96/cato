import logging

logger = logging.getLogger(__name__)


class OutputProcessor:
    def process(self, line: str) -> None:
        logger.info(line.strip())
