import logging
import time
from pathlib import Path


def get_logger(name: str, technical_name: str):
    logger = logging.getLogger(name)
    logging.basicConfig(filename=Path(__file__).parents[0].joinpath(r'.\Logs\debug.txt'),
                        filemode='a',
                        level=logging.INFO)
    if technical_name == '__main__':
        logger.info(f"Started {time.ctime()}")
    return logger
