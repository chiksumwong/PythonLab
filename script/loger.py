import logging
import os
from pathlib import Path
from config.settings import LOG_DIR

LOGGING_FILE = os.path.join(LOG_DIR, 'lob.log')

LOGGING_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y%m%d %H:%M:%S'

Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

logging.basicConfig(level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=DATE_FORMAT, filename=LOGGING_FILE, filemode='a+')


def log_debug(message):
    logging.debug(message)


def log_info(message):
    logging.info(message)


def log_exc(message):
    logging.error(message, exc_info=True)


def log_error(message):
    logging.error(message, exc_info=True)
