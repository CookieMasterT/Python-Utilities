import logging
import time
from pathlib import Path


class LoggerManager:
    Initialized = False

    def get_logger(self, name: str):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not self.Initialized:
            self.Initialized = True
            logger.info(f"Started {time.ctime()}")
            file_handler = logging.FileHandler(Path(__file__).parents[0].joinpath(r'.\Logs\debug.txt'), mode='a')
            console_handler = logging.StreamHandler()
            handlers = [file_handler, console_handler]

            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            for handler in handlers:
                handler.setLevel(logging.INFO)
                handler.setFormatter(formatter)
                logger.addHandler(handler)
        return logger
