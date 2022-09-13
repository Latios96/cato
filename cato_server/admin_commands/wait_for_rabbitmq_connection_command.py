import datetime

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
from kombu import Connection
import logging

from cato_server.configuration.parts.celery_configuration import CeleryConfiguration

logger = logging.getLogger(__name__)

MAX_TRIES = datetime.timedelta(minutes=5)
WAIT_BETWEEN = datetime.timedelta(seconds=1)


class WaitForRabbitMqConnectionCommand:
    def __init__(self, celery_configuration: CeleryConfiguration):
        self._celery_configuration = celery_configuration

    @retry(
        stop=stop_after_attempt(int(MAX_TRIES.total_seconds())),
        wait=wait_fixed(WAIT_BETWEEN.total_seconds()),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN),
    )
    def wait_for_connection(self) -> None:
        logger.info("Try to connect to RabbitMQ..")
        try:
            conn = Connection(self._celery_configuration.broker_url)
            conn.connect()
        except Exception as e:
            logger.error(e)
            raise e
