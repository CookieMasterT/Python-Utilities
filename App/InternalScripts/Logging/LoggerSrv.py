import logging
import time
from pathlib import Path


class LoggerManager:
    """
    Ensures logging is configured properly and only setup once
    This should be used as the only source of logging
    """
    Initialized = False

    def get_logger(self, name: str):
        """
        Returns a logger for the given name
        :param name: Name of the logger
        :return: Configured logger fom the logging module
        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        if not self.Initialized:
            self.Initialized = True
            logger.info(f"Started {time.ctime()}")
            file_handler = logging.FileHandler(Path(__file__).parents[0] / 'Logs/debug.txt', mode='a')
            console_handler = logging.StreamHandler()
            handlers = [file_handler, console_handler]

            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            for handler in handlers:
                handler.setLevel(logging.INFO)
                handler.setFormatter(formatter)
                logger.addHandler(handler)
        return logger
