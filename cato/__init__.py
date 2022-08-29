__version__ = "0.55.2"
import logging

# create logger with 'spam_application'
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter("[%(levelname)s]  %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
