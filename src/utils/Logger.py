import logging
import logging.handlers
from datetime import datetime
from pathlib import Path

LOG_PATH = Path(f'data/logs/{datetime.now().date()}.log')


def info(msg: str) -> None:
    logging.getLogger().info(msg)


def warn(msg: str) -> None:
    logging.getLogger().warning(msg)


def error(msg: str) -> None:
    logging.getLogger().error(msg)


def setup() -> logging.Logger:
    stdout_handler = logging.StreamHandler()
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_handler = logging.handlers.WatchedFileHandler(LOG_PATH)
    formatter = logging.Formatter(logging.BASIC_FORMAT)
    file_handler.setFormatter(formatter)
    stdout_handler.setFormatter(formatter)
    root = logging.getLogger()
    root.setLevel("INFO")
    root.addHandler(file_handler)
    root.addHandler(stdout_handler)
    return root
