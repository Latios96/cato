import datetime
from typing import Callable

from sqlalchemy.orm import Session
from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed
import logging

logger = logging.getLogger(__name__)

MAX_TRIES = datetime.timedelta(minutes=5)
WAIT_BETWEEN = datetime.timedelta(seconds=1)


class WaitForDbConnectionCommand:
    def __init__(self, session_maker: Callable[[], Session]):
        self._session_maker: Callable[[], Session] = session_maker

    @retry(
        stop=stop_after_attempt(int(MAX_TRIES.total_seconds())),
        wait=wait_fixed(WAIT_BETWEEN.total_seconds()),
        before=before_log(logger, logging.INFO),
        after=after_log(logger, logging.WARN),
    )
    def wait_for_connection(self) -> None:
        logger.info("Try to connect to database..")
        try:
            session = self._session_maker()
            session.execute("SELECT 1")
        except Exception as e:
            logger.error(e)
            raise e
