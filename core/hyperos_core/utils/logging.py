import logging
import sys

LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logging(name: str = "hyperos", level: int = logging.INFO) -> None:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(LOG_FORMAT, DATE_FORMAT))

    if not logger.handlers:
        logger.addHandler(handler)
