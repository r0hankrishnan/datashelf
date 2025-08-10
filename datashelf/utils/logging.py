import logging


def setup_logger(name: str, level: int = logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s")

    return logger
