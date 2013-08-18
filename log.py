#-*- coding:utf-8 -*-
import logging
import log_settings

class Log(object):
    def __init__(self):
        if log_settings.LOG_LEVEL.strip().upper() == 'DEBUG':
            self.level = logging.DEBUG
        elif log_settings.LOG_LEVEL.strip().upper() == 'INFO':
            self.level = logging.INFO
        elif log_settings.LOG_LEVEL.strip().upper() == 'WARNING':
            self.level = logging.WARNING
        elif log_settings.LOG_LEVEL.strip().upper() == 'ERROR':
            self.level = logging.ERROR
        else:
            raise Exception("not support log level ", log_settings.LOG_LEVEL)
            exit(-1)
        logging.basicConfig(format='%(levelname)s : %(asctime)s %(message)s', level=self.level)

    def log_debug(self, text):
        logging.debug(text)

    def log_info(self, text):
        logging.info(text)

    def log_warning(self, text):
        logging.warning(text)

    def log_error(self, text):
        logging.error(text)

logger = Log()

if __name__ == "__main__":
    logger.log_debug("debug")
    logger.log_info("info")
    logger.log_warning("warning")
    logger.log_error("error")
