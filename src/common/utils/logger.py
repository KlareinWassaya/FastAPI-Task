import logging
import os

from jsonformatter import JsonFormatter

from src.config.definitions import SERVICE_NAME

LOG_FORMAT = {
    "timestamp": "%(asctime)s",
    "name": "%(name)s",
    "level": "%(levelname)s",
    "module": "%(module)s",
    "filename_line": "%(filename)s:%(lineno)s",
    "message": "%(message)s",
}

logger_name = os.environ.get("logger_name", f"{SERVICE_NAME}_logs")
logger = logging.getLogger(logger_name)
logger.propagate = False
logger.setLevel(logging.INFO)

if not logger.hasHandlers():
    formatter = JsonFormatter(LOG_FORMAT)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    logger.addHandler(stream_handler)
