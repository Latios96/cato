__version__ = "0.69.0"
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s]  %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
