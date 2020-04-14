import logging
import logging.handlers
import os
from datetime import datetime

LOG_PATH = os.path.join('data', 'logs', f'{datetime.now().date()}.log')


def _setup_logger():
    stdout_handler = logging.StreamHandler()
    file_handler = logging.handlers.WatchedFileHandler(LOG_PATH)
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel("INFO")
    root.addHandler(file_handler)
    root.addHandler(stdout_handler)
    return root
