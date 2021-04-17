import logging
from logging.handlers import RotatingFileHandler

LOGGING_LEVEL = logging.INFO

logger = logging.getLogger("cato_server")
logger.setLevel(LOGGING_LEVEL)
ch = logging.StreamHandler()
ch.setLevel(LOGGING_LEVEL)
formatter = logging.Formatter(
    "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s"
)
ch.setFormatter(formatter)
logger.addHandler(ch)


def setup_file_handler(path: str, max_bytes, backup_count):
    logger.info("Adding RotatingFileHandler..")
    fh = RotatingFileHandler(path, maxBytes=max_bytes, backupCount=backup_count)
    fh.setLevel(LOGGING_LEVEL)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info(
        "Added RotatingFileHandler logging to %s. Log statements appear now in the file",
        path,
    )
