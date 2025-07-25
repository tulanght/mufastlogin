# file-path: src/core/app_logger.py
# version: 1.0
# last-updated: 2025-07-25
# description: Configures a shared logger for the application.

import logging
from logging.handlers import RotatingFileHandler
import sys

def setup_logger():
    logger = logging.getLogger("MUFastLoginLogger")
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(logging.INFO)
    stdout_handler.setFormatter(formatter)

    file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024, backupCount=3, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(stdout_handler)
    logger.addHandler(file_handler)
    return logger

log = setup_logger()