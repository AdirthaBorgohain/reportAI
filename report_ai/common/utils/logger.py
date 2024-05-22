import os
import sys
import time
import logging

from logging.handlers import RotatingFileHandler
from logging.handlers import TimedRotatingFileHandler


class Logger:
    def __init__(self, log_file_name: str, log_path: str):
        self.__log_file_path = os.path.join(log_path, log_file_name)

    def create_size_rotating_log(self, name="rotating", max_bytes=104857600, backup_count=10) -> logging:
        path = self.__log_file_path
        logger = logging.getLogger(f"{name} Log")
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.handlers.clear()
        logger.addHandler(sh)

        # add a rotating handler
        handler = RotatingFileHandler(path, maxBytes=max_bytes,
                                      backupCount=backup_count)
        logger.addHandler(handler)

        return logger

    def create_time_rotating_log(self, name="rotating", when="minute", interval=1, backup_count=10) -> logging:
        valid_when_params = {"minute": "m", "second": "s", "hour": "h", "day": "d", "midnight": "MIDNIGHT"}
        when = valid_when_params.get(when)
        if when is None:
            raise Exception("invalid when param")

        path = self.__log_file_path
        logger = logging.getLogger(f"{name} log")
        logger.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(formatter)
        logger.handlers.clear()
        logger.addHandler(sh)

        handler = TimedRotatingFileHandler(path,
                                           when=when,
                                           interval=interval,
                                           backupCount=backup_count)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger


if __name__ == '__main__':
    logger_handler = Logger(log_file_name="test.log", log_path="../../gene/logs")
    logger = logger_handler.create_time_rotating_log(when="second")
    for i in range(10):
        logger.info("This is test log line %s" % i)
        time.sleep(2)
